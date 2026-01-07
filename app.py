from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "changeme123")

@app.route("/")
def home():
    return "PC Command Server is running"

@app.route("/run", methods=["POST"])
def run_command():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    cmd = data.get("cmd")

    if not cmd:
        return jsonify({"error": "No command"}), 400

    try:
        result = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, timeout=5
        )
        return jsonify({"output": result.decode()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
