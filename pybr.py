import subprocess

def faceRecognition(photoPath1, photoPath2):
    """
    Runs the openbr process and returns the likeliness
    of the two faces as a float from 0.0 to 1.0. However
    for matching, you need to check if the result likelihood
    is equal to 1
    """
    output = subprocess.check_output(
        [
            'br',
            '-algorithm',
            'FaceRecognition',
            '-compare',
            photoPath1,
            photoPath2
        ]
    )

    return float(output.split("\n")[-2])
