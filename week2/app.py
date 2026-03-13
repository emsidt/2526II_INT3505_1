from flask import Flask, jsonify, request, make_response
from functools import wraps
from datetime import datetime, timedelta, UTC
import hashlib
import json
import jwt

app = Flask(__name__)

SECRET_KEY = "my_secret_key_123"
ALGORITHM = "HS256"

users = [
    {"id": 1, "name": "duong", "email": "duong@example.com"},
    {"id": 2, "name": "trinh", "email": "trinh@example.com"},
]

accounts = [
    {"username": "admin", "password": "123456", "role": "admin"},
    {"username": "user1", "password": "111111", "role": "user"},
]


def find_account(username):
    for account in accounts:
        if account["username"] == username:
            return account
    return None


def generate_token(account):
    payload = {
        "username": account["username"],
        "role": account["role"],
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


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


def generate_etag(data):
    json_data = json.dumps(data, sort_keys=True)
    return hashlib.md5(json_data.encode()).hexdigest()


def make_cache_response(data, max_age=60):
    etag = generate_etag(data)
    client_etag = request.headers.get("If-None-Match")

    if client_etag == etag:
        response = make_response("", 304)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = f"private, max-age={max_age}"
        return response

    response = make_response(jsonify(data), 200)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = f"private, max-age={max_age}"
    return response


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "User API server is running"}), 200


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    account = find_account(username)

    if not account or account["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(account)

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200


@app.route("/api/v1/users", methods=["GET"], strict_slashes=False)
@require_auth
def get_users():
    return make_cache_response(users, max_age=60)


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return make_cache_response(user, max_age=30)

    return jsonify({"error": "User not found"}), 404


@app.route("/api/v1/users", methods=["POST"], strict_slashes=False)
@require_auth
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400

    new_id = max((user["id"] for user in users), default=0) + 1

    new_user = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)

    return jsonify(new_user), 201


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
@require_auth
def update_user(user_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400

    for user in users:
        if user["id"] == user_id:
            user["name"] = data["name"]
            user["email"] = data["email"]
            return jsonify(user), 200

    return jsonify({"error": "User not found"}), 404


@app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
@require_auth
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return "", 204

    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)