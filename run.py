#Imports
import os
import time
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import cv2

#CONFIGS
UPLOAD_FOLDER = 'static\images'
PERMITTED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
IMAGE_SCALE = 1.5

#Flask Application Setup
app = Flask(__name__, static_url_path="", static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "Blooware is quite amazing :)"

#DIRECTORIES
ORIGINAL_IMAGES = os.path.join(app.config['UPLOAD_FOLDER'],"original")
MODIFIED_IMAGES = os.path.join(app.config['UPLOAD_FOLDER'],"modified")

#Flask Routing - Definition of pages and execution
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/images")
def images():
    modified_images = os.listdir(MODIFIED_IMAGES);

    #modified_images = ['images/modified/' + file for file in modified_images]
    return render_template('images.html', modified_images=modified_images)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in PERMITTED_EXTENSIONS

@app.route("/image_upload", methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        if 'image_file' not in request.files:
            flash('No file part')
            return redirect(url_for("index"))

        file = request.files['image_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("index"))

        if file and allowed_file(file.filename):
            check = True
            counter = 0
            while check:
                filename = str(counter) + "_" + file.filename
                file_to_check = os.path.join(ORIGINAL_IMAGES, secure_filename(filename))
                if os.path.exists(file_to_check):
                    counter = counter + 1
                else:
                    check = False

            temp_target = os.path.join(ORIGINAL_IMAGES, secure_filename(filename))
            file.save(temp_target)
            img = cv2.imread(temp_target, cv2.IMREAD_UNCHANGED)

            width = int(img.shape[1] * IMAGE_SCALE)
            height = int(img.shape[0] * IMAGE_SCALE)
            dim = (width, height)

            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            filename = str(counter) + "_" + file.filename
            target = os.path.join(MODIFIED_IMAGES, secure_filename(filename))
            cv2.imwrite(target, resized)
            flash(str(filename))
        return redirect(url_for("images"))
    else:
        flash("Please use this form to upload images.")
        return redirect(url_for("index"))

#Start Flask Server
if __name__ == "__main__":
    app.run()
