from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "duong", "email": "duong@example.com"},
    {"id": 2, "name": "trinh", "email": "trinh@example.com"},
]

@app.route("/")
def home():
    return jsonify({"message": "User API server is running"})

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "sai ten hoac email"}), 400
    new_id = max(user["id"] for user in users) + 1 if users else 1

    new_user = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)
    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run(debug=True)