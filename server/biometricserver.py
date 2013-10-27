import os
import pybr
import cv2
import sys
import config
import base64
from flask import Flask, request, redirect, url_for, abort, jsonify

"""
Biometrics server for image authentication
"""

app = Flask(__name__)

def getHist(img):
    """
    Returns the image color histogram
    """
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist(
        imgHSV,
        [0, 1],
        None,
        [180, 256],
        [0, 180, 0, 256]
    )
    cv2.normalize(hist, hist, cv2.NORM_MINMAX)
    return hist

def checkSimilarity(imagePath1, imagePath2):
    """
    Checks the correlation similarity of the two images
    using compareHist
    """
    image1 = cv2.imread(imagePath1)
    image2 = cv2.imread(imagePath2)

    hist1 = getHist(image1)
    hist2 = getHist(image2)

    return cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CORREL)

@app.route('/check/<int:userId>', methods = ['POST'])
def postCheck64(userId):
    """

    Checks if an image passed to the server biometrically matches
    with the image stored as the userId.

    Parameters:
        userId: <int: id of user>

    Form data:
    {
        image: <Base 64 Image>
    }

    Returns:
        On Success: {
            response_code: <int: 200>,
            similarity_metric: <float: f between [0, 1]>,
            hist_similarity: <float: f between [0, 1]>
        }

        On Failure: {
            response_code: <int: 500>
        }

    """
    try:
        if not os.path.exists(config.tempDir):
            os.mkdir(config.tempDir)

        storedPath = os.path.join(
            config.referenceDir,
            str(userId) + config.imageExtension
        )

        if not os.path.exists(storedPath):
            raise Exception()

        image64 = request.form[config.imageFieldName]
        image = base64.b64decode(image64)
        tempPath = os.path.join(
            config.tempDir,
            str(userId) + config.imageExtension
        )
        tempImage = open(
            tempPath, 'wb'
        )
        tempImage.write(image)
        tempImage.close()

        histogramSimilarity = checkSimilarity(tempPath, storedPath)

        similarity = pybr.faceRecognition(tempPath, storedPath)
        print "Similarity:", similarity
        print "Hist Similarity:", histogramSimilarity
        return jsonify(
            response_code = config.okCode,
            similarity_metric = similarity,
            hist_similarity = histogramSimilarity
        ), config.okCode
    except:
        return jsonify(
            response_code = config.errorCode
        ), config.errorCode


@app.route('/reference/<int:userId>', methods = ['POST'])
def postReference64(userId):
    import traceback
    """

    Creates a new reference image of somebody using biauthorize

    Parameters:
        userId: <int: id of user>

    Form data:
    {
        image: <Base 64 Image>
    }

    Returns:
        On Success: 200
        On Error: 500

    """
    try:
        if not os.path.exists(config.referenceDir):
            os.mkdir(config.referenceDir)

        image64 = request.form[config.imageFieldName]
        decodedImage = base64.b64decode(image64)
        imageFile = open(
            os.path.join(
                config.referenceDir,
                str(userId) + config.imageExtension
            ), 'wb'
        )

        imageFile.write(decodedImage)
        imageFile.close()
        return jsonify(
            response_code = config.okCode
        ), config.okCode
    except:
        return jsonify(
            response_code = config.errorCode
        ), config.errorCode

if __name__ == "__main__":
    if len(sys.argv) < 3:
        app.run(debug = True)
    else:
        app.run(
            host = sys.argv[1],
            port = int(sys.argv[2]),
            debug = True
        )
