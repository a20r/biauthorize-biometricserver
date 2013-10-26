import os
import sys
import config
from flask import Flask, request, redirect, url_for, abort

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/check/<userId>', methods = ['POST'])
def postCheck(userId):
    filename = request.files[config.imageFieldName]

@app.route('/reference/<userid>', method = 'POST')
def reference(userId):
    filename = request.files[config.imageFieldName]

    if filename:
        try:
            newfile = open(
                os.path.join(
                    config.referenceDir,
                    str(userid) + imageExtension
                ), "w"
            )
            newfile.write()
            newfile.close()
            return config.okCode
        except:
            return config.errorCode

if __name__ == "__main__":
    if len(sys.argv) < 3:
        app.run()
    else:
        app.run(host = sys.argv[1], port = int(sys.argv[2]))
