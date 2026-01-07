from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "PC Command Server is running"

@app.route("/run", methods=["POST"])
def run_command():
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
