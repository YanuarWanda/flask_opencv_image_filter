from flask import Blueprint, render_template, request, make_response
import cv2
import numpy as np

def grayscale(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grayscale

def setBrighness(img, beta_value):
    result = cv2.convertScaleAbs(img, beta = beta_value)
    return result

views = Blueprint("views", __name__)

@views.route("/", methods = ['GET', 'POST'])
def home():
    if (request.method == "POST"):
        if not request.files:
            return make_response({ "status": "error" }), 400

        imageBuffer = request.files["image"].read()
        data = np.frombuffer(imageBuffer, np.uint8)
        image = cv2.imdecode(data, 1)

        filter = request.form.get("filter")
        if (filter == "1"):
            result = grayscale(image)
        elif (filter == "2"):
            result = setBrighness(image, 60)
        elif (filter == "3"):
            result = setBrighness(image, -60)

        image = cv2.imencode('.png', result)[1]

        return make_response(image.tobytes())
    else:
        return render_template("home.html")