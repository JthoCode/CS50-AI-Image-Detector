from flask import Flask, render_template, request
from detector import predict_image

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "GET":
        return render_template("index.html")

    image = request.files.get("image-upload")

    if image is None or image.filename == "":
        return "403 ERROR! Image not inputted", 403

    image.save("temp.jpg")

    result = predict_image("temp.jpg")

    prediction = result["prediction"]
    confidence = result["confidence"]

    prediction = result["prediction"]
    confidence = result["confidence"]

    if prediction == "human":
        label="Human"
        color="green"
    elif confidence < 50 and prediction == "human":
        label="Human"
        color="yellow"
    elif confidence < 50 and prediction == "ai":
        label="AI"
        color="yellow"
    else:
        label="AI"
        color="red"

    return render_template(
        "output.html",
        confidence=confidence,
        label=label,
        color=color
    )

@app.route("/how-it-works")
def work():
    return render_template("work.html")

@app.route("/sample/<filename>")
def sample(filename):
    allowed = {"ai1.jpg", "human1.jpg", "ai2.jpg"}

    if filename not in allowed:
        return "Invalid sample", 404
    
    result = predict_image(f"static/samples/{filename}")

    prediction = result["prediction"]
    confidence = result["confidence"]

    if prediction == "human":
        label="Human"
        color="green"
    elif confidence < 50 and prediction == "human":
        label="Human"
        color="yellow"
    elif confidence < 50 and prediction == "ai":
        label="AI"
        color="yellow"
    else:
        label="AI"
        color="red"

    return render_template(
        "output.html",
        confidence=confidence,
        label=label,
        color=color
    )

@app.route("/debug")
def debug():
    return {
        "files": str(request.files),
        "form": str(request.form)
    }