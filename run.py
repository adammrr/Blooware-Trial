#Imports
import os
import time
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import cv2

#Image Upload Configs.
UPLOAD_FOLDER = 'images'
PERMITTED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#Flask Application Setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "Blooware is quite amazing :)"

#Flask Routing - Definition of pages and execution
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/images")
def images():
    images = os.path.listdir('static/images')
    print(os.path.listdir('static/images'))
    return render_template('images.html', images = images)

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
                filename =  "original_" + str(counter) + "_" + file.filename
                file_to_check = os.path.join(app.config['UPLOAD_FOLDER'],"original", secure_filename(filename))
                if os.path.exists(file_to_check):
                    counter = counter + 1
                else:
                    check = False

            temp_target = os.path.join(app.config['UPLOAD_FOLDER'],"original", secure_filename(filename))
            file.save(temp_target)
            img = cv2.imread(temp_target, cv2.IMREAD_UNCHANGED)

            scale_percent = 150
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)

            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            filename = "modified_" + str(counter) + "_" + file.filename
            target = os.path.join(app.config['UPLOAD_FOLDER'],"modified", secure_filename(filename))
            cv2.imwrite(target, resized)
            flash("Your image is located at " + str(target))
        return render_template('images.html')
    else:
        flash("Please use this form to upload images.")
        return redirect(url_for("index"))

#Start Flask Server
if __name__ == "__main__":
    app.run()
