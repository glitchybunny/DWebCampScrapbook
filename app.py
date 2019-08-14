"""

    A local web app that allows images to be uploaded (and eventually backed up to archive.org)
    Author: Riley Taylor (https://rtay.io/)
    Last modified: 2019/08/15
    Python version: 3.7

"""

import os
from flask import Flask, render_template, request, redirect, session, make_response, Blueprint
from werkzeug.utils import secure_filename
import time
import json

#import pyexiv2  # pyexiv2 doesn't seem to have support for the raspberry pi we're running the code on, so I will have to find another alternative
#import requests
#import internetarchive

def allowed_file(filename):  # tests file extension and compares against list of allowed extensions
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS
    #return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def ensure_dir(f):  # checks if directory exists, and creates it if it doesn't
    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)

def add_metadata(filename, artist, desc):  # Add metadata to image file
    filename_json = os.path.splitext(filename)[0]+'.json'

    with open(filename_json, 'w') as f:
        json.dump({'Exif.Image.Artist':artist, "Exif.Image.ImageDescription":desc}, f)

    """ # This is currently completely broken
    im = pyexiv2.Image(filename)  
    exif = im.read_exif()
    exif['Exif.Image.Artist'] = artist
    exif['Exif.Image.ImageDescription'] = desc
    im.modify_exif(exif)
    """


# Setup flask stuff
app = Flask(__name__, static_url_path="")

@app.route('/upload', methods=['POST'])
def handle_form():
    file = request.files['file']

    data_dir = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'])
    ensure_dir(data_dir)

    save_path = os.path.join(data_dir, secure_filename(file.filename))
    current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        return make_response(('File already exists', 400))

    try:
        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        print('Could not write to file')
        return make_response(("Not sure why, but we couldn't write the file to disk", 500))

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
            print(f"File {file.filename} was completed, but has a size mismatch. Was {os.path.getsize(save_path)} but we expected {request.form['dztotalfilesize']} ")
            return make_response(('Size mismatch', 500))
        else:
            print(f'File {file.filename} has been uploaded successfully')
    else:
        print(f'Chunk {current_chunk + 1} of {total_chunks} for file {file.filename} complete')

    return make_response(("Chunk upload successful", 200))

    """
    # check if the post request has the file part
    if 'file' not in data:
        print("Redirecting to request URL")
        return redirect(request.url)

    # get list of files sent through
    uploaded_files = data.getlist("file")

    if (len(uploaded_files)) == 0:
        print("Redirecting to request URL")
        return redirect(request.url)

    # get metadata from request and sort into lists
    names = []
    descs = []
    for key in request.form.keys():
        if key.startswith('name_'):
            names.append(request.form[key])
        elif key.startswith('desc_'):
            descs.append(request.form[key])

    # loop through and save all uploaded files to temp directory
    upload_time = str(round(time.time()))
    upload_path = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'])
    ensure_dir(upload_path)

    files_to_process = []
    for each_file in uploaded_files:
        if each_file and allowed_file(each_file.filename):
            filename = secure_filename(each_file.filename)
            filepath = upload_path + upload_time + "_" + filename
            each_file.save(filepath)
            files_to_process.append(filepath)

    # now make filenames unique and save files to uploaded directory
    num_files = len(files_to_process)
    print("Batch size: " + str(num_files))

    if num_files == 0:
        # redirect if none of the files are uploaded correctly
        return error("None of your files were able to upload<br/>Please check your network connection and try again")

    elif num_files >= 1:
        # otherwise process all the files asynchronously so request doesn't time out
        for i in range(len(files_to_process)):
            # add metadata to image file
            add_metadata(files_to_process[i], names[i], descs[i])

    # redirect to upload successful page
    return index(True)"""


@app.route("/")
def index(success=False):
    return render_template("index.html", SUCCESS = success);


if __name__ == '__main__':
    # Initialise all important variables and config
    UPLOAD_FOLDER = '/uploads/'
    ALLOWED_EXTENSIONS = ['.jpe','.jpg','.jpeg','.gif','.png','.bmp','.ico','.svg','.svgz','.tif','.tiff','.ai','.drw','.pct','.psp','.xcf','.psd','.raw']

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'

    # App execution code
    if os.getenv('DEBUG', False):
        app.run(host='0.0.0.0', port=80, debug=False)  # Test on localhost
    else:
        app.run(host='10.8.8.8', port=88, debug=False)  # Run on specific mesh IP
