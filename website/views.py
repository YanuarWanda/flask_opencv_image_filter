from flask import Blueprint, render_template, request, make_response
import cv2
import numpy as np

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def setBrighness(img, beta_value):
    return cv2.convertScaleAbs(img, beta = beta_value)

def bilateralBlur(img, diameter, sigmaColor, sigmaSpace):
    return cv2.bilateralFilter(img, diameter, sigmaColor, sigmaSpace)

def gaussianBlur(img, kSize, sigmaX):
    return cv2.GaussianBlur(img, kSize, sigmaX)

def laplasianFilter(img):
    return cv2.Laplacian(grayscale(img), cv2.CV_8UC4, ksize=5)

def sobel(img, x, y):
    return cv2.Sobel(gaussianBlur(grayscale(img), (3, 3), 0), cv2.CV_64F, x, y, ksize=5)

def canny(img):
    return cv2.Canny(img, 100, 200)

def averagingBlur(img, kSize):
    return cv2.blur(img, kSize)

def medianBlur(img, kSize):
    return cv2.medianBlur(img, kSize)

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
        elif (filter == "4"):
            result = laplasianFilter(image)
        elif (filter == "5"):
            result = sobel(image, 1, 0)
        elif (filter == "6"):
            result = sobel(image, 0, 1)
        elif (filter == "7"):
            result = sobel(image, 1, 1)
        elif (filter == "8"):
            result = canny(image)
        elif (filter == "9"):
            result = averagingBlur(image, (9, 9))
        elif (filter == "10"):
            result = gaussianBlur(image, (9, 9), 0)
        elif (filter == "11"):
            result = medianBlur(image, 9)
        elif (filter == "12"):
            result = bilateralBlur(image, 25, 75, 75)

        image = cv2.imencode('.png', result)[1]

        return make_response(image.tobytes())
    else:
        return render_template("home.html")