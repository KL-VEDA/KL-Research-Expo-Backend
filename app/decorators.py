from functools import wraps
from flask import request, jsonify, current_app
import jwt

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"success": False, "message": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]  # "Bearer <token>"
            decoded = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            # Pass decoded info to the route if needed
            return f(decoded, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token"}), 401

    return decorated
