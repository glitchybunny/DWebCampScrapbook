import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import requests
import internetarchive

# Initialise all the main stuff
UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = {'jpg','png'}

app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('FLASK_SECRET_KEY')


# Just some misc functions I copied from other project code that I'll document later
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)


# Do the flask
@app.route('/upload', methods=['POST'])
def handle_form():
    if request.method == 'POST':
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

        # loop through and save all uploaded files
        files_to_process = []
        upload_path = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'])
        ensure_dir(upload_path)

        files_to_process = []
        for each_file in uploaded_files:
            if each_file and allowed_file(each_file.filename):
                filename = secure_filename(each_file.filename)
                try:
                    each_file.save(upload_path + filename)
                    files_to_process.append(upload_path + filename)
                except PermissionError:
                    return error("PermissionError - can't get write access?<br/>Maybe speak to one of the Network Stewards about this (preferrably Riley)")

        # now do the processing
        num_files = len(files_to_process)

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


if __name__ == "__main__":
    # app.run(host='10.8.8.8', port=88, debug=False)  # Run on specific mesh IP
    app.run(host='0.0.0.0', port=80, debug=True)  # Test on localhost