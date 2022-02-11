from flask import Blueprint, render_template, request, json, make_response
import cv2
import numpy as np
import base64

def grayscale(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grayscale

views = Blueprint("views", __name__)

@views.route("/", methods = ['GET', 'POST'])
def home():
    if (request.method == "POST"):
        imageBuffer = request.files["image"].read()
        data = np.frombuffer(imageBuffer, np.uint8)
        image = cv2.imdecode(data, 1)

        filter = request.form.get("filter")
        match filter:
            case "1":
                result = grayscale(image)

        image = cv2.imencode('.png', result)[1]

        return make_response(image.tobytes())
    else:
        return render_template("home.html")