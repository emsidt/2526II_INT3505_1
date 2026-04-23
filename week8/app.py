from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake in-memory database
products = [
    {
        "id": 1,
        "name": "Laptop Lenovo",
        "price": 15000000,
        "description": "Laptop for study",
        "category": "Electronics",
        "stock": 10
    },
    {
        "id": 2,
        "name": "Chuot Logitech",
        "price": 350000,
        "description": "Wireless mouse",
        "category": "Accessories",
        "stock": 25
    }
]

VALID_USERNAME = "admin"
VALID_PASSWORD = "123456"
FAKE_TOKEN = "fake-jwt-token-123"

def find_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Buoi 8 API Testing Demo is running",
        "endpoints": [
            "POST /auth/login",
            "GET /products",
            "GET /products/<id>",
            "POST /products",
            "DELETE /products/<id>"
        ]
    }), 200

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({
            "message": "Login successful",
            "token": FAKE_TOKEN
        }), 200

    return jsonify({
        "message": "Invalid username or password"
    }), 401

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = find_product(product_id)
    if product:
        return jsonify(product), 200

    return jsonify({
        "message": f"Product with id {product_id} not found"
    }), 404

@app.route("/products", methods=["POST"])
def create_product():
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {FAKE_TOKEN}":
        return jsonify({
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    required_fields = ["name", "price", "description", "category", "stock"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "message": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    try:
        new_id = max([p["id"] for p in products], default=0) + 1
        new_product = {
            "id": new_id,
            "name": data["name"],
            "price": data["price"],
            "description": data["description"],
            "category": data["category"],
            "stock": data["stock"]
        }
        products.append(new_product)

        return jsonify({
            "message": "Product created successfully",
            "product": new_product
        }), 201
    except Exception as e:
        return jsonify({
            "message": "Error creating product",
            "error": str(e)
        }), 500

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {FAKE_TOKEN}":
        return jsonify({
            "message": "Unauthorized"
        }), 401

    product = find_product(product_id)
    if not product:
        return jsonify({
            "message": f"Product with id {product_id} not found"
        }), 404

    products.remove(product)
    return jsonify({
        "message": "Product deleted successfully",
        "deleted_product": product
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)