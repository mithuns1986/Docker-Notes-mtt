#!/usr/bin/env python3

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/launch_container', methods=['POST'])
def launch_container():
    # Obtain container details from the request payload
    data = request.json
    cname = data.get("d1")
    cimage = data.get("d2")

    if not cname or not cimage:
        return jsonify({"message": "Container name and image are required"}), 400

    cmd = f"sudo docker run -dit --name {cname} {cimage}"
    status, out = subprocess.getstatusoutput(cmd)

    if status == 0:
        return jsonify({"message": f"Container {cname} launched successfully"})
    else:
        return jsonify({"message": f"Error launching Container: {out}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
