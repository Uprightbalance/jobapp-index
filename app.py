from flask import Flask, request, redirect, send_from_directory, abort
import boto3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --------------------
# Configuration
# --------------------
BUCKET_NAME = os.environ.get("CV_BUCKET_NAME", "jobapp-cv-bucket-upright01")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Limit upload size to 5MB (good practice)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  

# --------------------
# AWS S3 Client
# (uses IAM Role attached to EC2)
# --------------------
s3 = boto3.client("s3", region_name=AWS_REGION)

# --------------------
# Routes
# --------------------

@app.route("/", methods=["GET"])
def home():
    try:
        return send_from_directory(".", "index.html")
    except FileNotFoundError:
        abort(404)

# ALB health check endpoint (CRITICAL)
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/apply", methods=["POST"])
def apply():
    if "cv" not in request.files:
        return "No file part in request", 400

    file = request.files["cv"]

    if file.filename == "":
        return "No file selected", 400

    # Secure the filename
    safe_filename = secure_filename(file.filename)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    s3_key = f"applications/{timestamp}_{safe_filename}"

    try:
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        return f"Upload failed: {str(e)}", 500

    return "Application submitted successfully!", 200


# --------------------
# Local development only
# (NOT used when running with Gunicorn)
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
