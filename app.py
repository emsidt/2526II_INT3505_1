from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

users = [
    {"id": 1, "name": "duong", "email": "duong@example.com"},
    {"id": 2, "name": "trinh", "email": "trinh@example.com"},
]

VALID_TOKEN = "mysecrettoken"


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Invalid authorization format"}), 401

        token = auth_header.split(" ")[1]

        if token != VALID_TOKEN:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return jsonify({"message": "User API server is running"})


@app.route("/users", methods=["GET"], strict_slashes=False)
@require_auth
def get_users():
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"], strict_slashes=False)
@require_auth
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400

    new_id = max(user["id"] for user in users) + 1 if users else 1

    new_user = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
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


@app.route("/users/<int:user_id>", methods=["DELETE"])
@require_auth
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return "", 204

    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)