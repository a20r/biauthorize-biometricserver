import os
import pybr
import sys
import config
from flask import Flask, request, redirect, url_for, abort

app = Flask(__name__)

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

        tempImage = open(
            tempPath, "wb"
        )

        storedPath = os.path.join(
            config.referenceDir,
            str(userId) + config.imageExtension
        )

        tempImage.write(sentImage)
        tempImage.close()

        similarity = pybr.faceRecognition(tempPath, storedPath)
        return flask.jsonify(
            response_code = config.okCode,
            similarity_metric = similarity
        )

    except KeyError:
        return config.errorCode

@app.route('/reference/<int:userId>', method = 'POST')
def reference(userId):
    """
    Used for initial storage of the reference image

    Returns: On success: 200, On failure: 500

    """
    try:
        image = request.files[config.imageFieldName]
        newImage = open(
            os.path.join(
                config.referenceDir,
                str(userId) + config.imageExtension
            ), "wb"
        )
        newImage.write(image)
        newImage.close()
        return config.okCode
    except:
        return config.errorCode

if __name__ == "__main__":
    if len(sys.argv) < 3:
        app.run()
    else:
        app.run(host = sys.argv[1], port = int(sys.argv[2]))
