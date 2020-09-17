import os

from flask import Flask, render_template, request, Response

import cv2

from wb import VideoCamera

app = Flask(__name__)

upload_location = 'static/images'
app.config['UPLOAD_FOLDER'] = upload_location
app.secret_key = "secret-key"
@app.route("/")
def homapage():
    return render_template("demo.html")

@app.route("/videoframe")
def homapage1():
    return render_template("videofeed.html")

@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
    if (request.method == 'POST'):
        f = request.files['file']
        filename = f.filename
        path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        f.save(path)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Read the input image
        img = cv2.imread(path)

        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.6, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # Display the output
        cv2.imwrite('.\static\predict\{}'.format(filename), img)

        return render_template("demo.html", fileupload=True, img_name=filename)

def gen(camera):
    while True:
        data = camera.get_frame()
        frame = data[0]
        yield(b'--frame\r\n'b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/imagedetect")
def imagedetect():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Read the input image
    img = cv2.imread('static/images/2.jpg')
     # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
    # Display the output
    cv2.imshow('Output', img)
    cv2.waitKey()
    return render_template("demo.html")
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8000', debug=True)


