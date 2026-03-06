from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

@app.route("/")
def home():
    return jsonify({"message": "User API server is running"})

@app.route("/getUsers", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/getUser/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)