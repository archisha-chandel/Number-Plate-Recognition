import os
import urllib.request

# from app import app
from flask import Flask, flash, request, redirect, render_template, send_file, url_for
from werkzeug.utils import secure_filename
from flask import Flask
from NUMBER-PLATE-RECOGNITION import main as detect
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

UPLOAD_FOLDER = './static'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['jpg','png'])
file_path = ''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def lca_file():
    if request.method == 'POST':
        # print("got post")
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER']+'/' + filename)
            # print("file uploaded")
            detect(file_path)
            # print("displaying")

            return render_template('results.html')
        else:
            flash('Allowed file types are of the format csv')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
