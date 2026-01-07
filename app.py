import os
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "changeme123")

@app.route("/")
def home():
    return "PC Command Server is running"

@app.route("/run", methods=["POST"])
def run_command():
    auth = request.headers.get("Authorization")
    if not auth or auth != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    cmd = data.get("cmd")

    if not cmd:
        return jsonify({"error": "No command"}), 400

    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output}), 500


# 🔴 BẮT BUỘC PHẢI CÓ
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
