from flask import Flask, jsonify, request, render_template, send_from_directory
from numba.typed.dictobject import new_dict
from pandas.core.internals.blocks import new_block

app = Flask(__name__)

books = [
{"id": 1, "title": "Lập trình REST", "author": "Anh", "published_year": 2024},
    {"id": 2, "title": "Microservices cơ bản", "author": "Cuong", "published_year": 2023},
    {"id": 3, "title": "Thiết kế API", "author": "An", "published_year": 2025},
]

def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
        return None

@app.route("/")
def home():
    return jsonify({
        "message": "Book API is running",
        "docs": "http://localhost:5000/docs"
    })
@app.route("/docs")
def swagger_ui():
    return render_template("swagger.html")

@app.route("/openapi.yaml")
def openapi_yaml():
    return send_from_directory(".", "openapi.yaml")

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    if not data:
        return jsonify({"error": "request body must be json"}), 400
    title = data.get("title")
    author = data.get("author")
    published_year = data.get("published_year")

    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400
    new_id = max(book["id"] for book in books) + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "published_year": published_year
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title")
    author = data.get("author")
    published_year = data.get("published_year")

    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400

    book["title"] = title
    book["author"] = author
    book["published_year"] = published_year

    return jsonify(book), 200


# 5. DELETE /books/<id> - xóa sách
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    return jsonify({"message": "Book deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
