import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import time
#import requests
#import internetarchive

def allowed_file(filename):  # tests file extension and compares against list of allowed extensions
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS
    #return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def ensure_dir(f):  # checks if directory exists, and creates it if it doesn't
    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)


# Setup flask stuff
app = Flask(__name__, static_url_path="")

@app.route('/upload', methods=['POST'])
def handle_form():
    if request.method == 'POST':

        print(request.form)

        session['output_path'] = ""

        # check if the post request has the file part
        if 'file' not in request.files:
            print("Redirecting to request URL")
            return redirect(request.url)

        # get list of files sent through from jquery
        uploaded_files = request.files.getlist("file")

        if (len(uploaded_files)) == 0:
            print("Redirecting to request URL")
            return redirect(request.url)

        # loop through and save all uploaded files to temp directory
        upload_time = str(round(time.time()))
        upload_path = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'])
        ensure_dir(upload_path)

        files_to_process = []
        for each_file in uploaded_files:
            if each_file and allowed_file(each_file.filename):
                filename = secure_filename(each_file.filename)
                try:
                    filepath = upload_path + upload_time + "_" + filename
                    each_file.save(filepath)
                    files_to_process.append(filepath)
                except PermissionError:
                    return error("PermissionError - can't get write access?<br/>Maybe speak to one of the Network Stewards about this (preferrably Riley)")

        # now make filenames unique and save files to uploaded directory
        num_files = len(files_to_process)
        print("Batch size: " + str(num_files))

        if num_files == 0:
            # redirect if none of the files are uploaded correctly
            return error("None of your files were able to upload<br/>Please check your network connection and try again")

        elif num_files >= 1:
            # otherwise process all the files normally
            for current_file in files_to_process:
                try:
                    print(current_file)
                except KeyError:
                    return error("KeyError when uploading {} files<br/>Filename: {}".format(num_files, current_file))

        # redirect to upload successful page
        return index(True)

@app.route("/error")
def error(error_code):
    return render_template("error.html", ERROR_CODE = error_code)

@app.route("/")
def index(success=False):
    return render_template("index.html", SUCCESS = success);


if __name__ == '__main__':

    # Initialise all important variables and config
    TEMP_FOLDER = '/temp/'
    UPLOAD_FOLDER = '/uploads/'
    ALLOWED_EXTENSIONS = ['.jpe','.jpg','.jpeg','.gif','.png','.bmp','.ico','.svg','.svgz','.tif','.tiff','.ai','.drw','.pct','.psp','.xcf','.psd','.raw']

    app.config['TEMP_FOLDER'] = TEMP_FOLDER
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', '42069') # please ensure the secret key is being set properly
    app.config['SESSION_TYPE'] = 'filesystem'

    # App execution code
    if os.getenv('DEBUG', False):
        app.run(host='0.0.0.0', port=80, debug=True)  # Test on localhost
    else:
        app.run(host='10.8.8.8', port=88, debug=False)  # Run on specific mesh IP
