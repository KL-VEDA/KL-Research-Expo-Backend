from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask API!"})

@main.route("/server_status")
def server_status():
    return jsonify({"status": True, "message": "Server is running!"})
