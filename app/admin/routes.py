from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from app.decorators import jwt_required

admin = Blueprint('admin', __name__)

# Temporary credentials (replace with DB later)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Secret key for JWT (set in main.py via app.config)
# Example: app.config['SECRET_KEY'] = "super-secret-key"

@admin.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # ✅ Generate JWT token
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1h expiry
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return jsonify({"success": True, "message": "Login successful", "token": token})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401


@admin.route('/protected', methods=['GET'])
@jwt_required
def protected(decoded):
    # Ensure only the admin username can access
    if decoded['username'] != "admin":
        return jsonify({"success": False, "message": "Unauthorized user"}), 403
    return jsonify({"success": True, "message": f"Welcome {decoded['username']}!"})
