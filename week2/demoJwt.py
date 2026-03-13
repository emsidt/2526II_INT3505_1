from functools import wraps
from datetime import datetime, timedelta, UTC

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

SECRET_KEY = "duong123"
ALGORITHM = "HS256"

users = [
    {"id": 1, "username": "admin", "password": "123456", "role": "admin"},
    {"id": 2, "username": "user1", "password": "111111", "role": "user"}
]


def find_user_by_username(username):
    for user in users:
        if user["username"] == username:
            return user
    return None


def generate_token(user):
    payload = {
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid authorization format"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = find_user_by_username(username)

    if not user or user["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(user)

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200


@app.route("/api/v1/profile", methods=["GET"])
@require_auth
def get_profile():
    return jsonify({
        "message": "Access granted",
        "user": request.user
    }), 200


@app.route("/api/v1/users", methods=["GET"])
@require_auth
def get_users():
    return jsonify([
        {"id": user["id"], "username": user["username"], "role": user["role"]}
        for user in users
    ]), 200


if __name__ == "__main__":
    app.run(debug=True)