from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "An", "email": "an@example.com"},
    {"id": 2, "name": "Binh", "email": "binh@example.com"},
    {"id": 3, "name": "Trinh", "email": "trinh@example.com"}
]

def find_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    name_filter = request.args.get("name")

    if name_filter:
        filtered_users = [
            user for user in users
            if name_filter.lower() in user["name"].lower()
        ]
        return jsonify(filtered_users), 200

    return jsonify(users), 200


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    if "name" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields: name, email"}), 400

    new_id = max([user["id"] for user in users], default=0) + 1

    new_user = {
        "id": new_id,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)

    return jsonify({
        "message": "User created successfully",
        "data": new_user
    }), 201


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = find_user(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])

    return jsonify({
        "message": "User updated successfully",
        "data": user
    }), 200


@app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = find_user(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)

    return jsonify({
        "message": f"User {user_id} deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)