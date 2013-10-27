import os
import pybr
import cv2
import sys
import config
from flask import Flask, request, redirect, url_for, abort, jsonify

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
def postCheck(userId):
    """
    Used to check if the sent image matches the image
    saved for the userId

    Returns: {
        response_code: <int (On error: 500, On success: 200)>,
        similarity_metric: <float (Total match: 1, Total mismatch: 0)>
    }
    """
    try:
        sentImage = request.files[config.imageFieldName]
        tempPath = os.path.join(
            config.tempDir,
            str(userId) + config.imageExtension
        )

        sentImage.save(tempPath)

        storedPath = os.path.join(
            config.referenceDir,
            str(userId) + config.imageExtension
        )

        histogramSimilarity = checkSimilarity(tempPath, storedPath)

        similarity = pybr.faceRecognition(tempPath, storedPath)
        return jsonify(
            response_code = config.okCode,
            similarity_metric = similarity,
            hist_similarity = histogramSimilarity
        )

    except KeyError:
        return jsonify(
            response_code = config.errorCode
        )

@app.route('/reference/<int:userId>', methods = ['POST'])
def postReference(userId):
    """
    Used for initial storage of the reference image

    Returns: On success: 200, On failure: 500

    """
    try:
        image = request.files[config.imageFieldName]
        print image
        image.save(
            os.path.join(
                config.referenceDir,
                str(userId) + config.imageExtension
            )
        )

        return jsonify(
            response_code = config.okCode
        )
    except:
        return jsonify(
            response_code = config.errorCode
        )

@app.route('/test/', methods = ['POST'])
def test():
    import base64
    try:
        image = request.form[cnofig.imageFieldName]
        decodedImage = base64.decode(image)
        imageFile = open(
            os.path.join(
                config.referenceDir,
                str("TEST") + config.imageExtension
            ), 'wb'
        )

        imageFile.write(decodedImage)
    except:
        pass

    print "Image:", image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        app.run()
    else:
        app.run(host = sys.argv[1], port = int(sys.argv[2]), debug = True)
