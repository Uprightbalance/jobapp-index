from flask import Flask, request, redirect
import boto3
import os
from datetime import datetime

app = Flask(__name__)

BUCKET_NAME = "jobapp-cv-bucket-upright01"

s3 = boto3.client("s3")

@app.route("/", methods=["GET"])
def home():
    return open("index.html").read()

@app.route("/apply", methods=["POST"])
def apply():
    file = request.files["cv"]
    if file.filename == "":
        return "No file selected", 400

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"applications/{timestamp}_{file.filename}"

    s3.upload_fileobj(file, BUCKET_NAME, filename)

    return "Application submitted successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
