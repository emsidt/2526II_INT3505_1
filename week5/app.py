from flask import Flask, jsonify, request
from page_based import paginate_page_based
from offset_limit import paginate_offset_limit
from cursor import paginate_cursor

app = Flask(__name__)

books = [
    {"id": 1, "title": "Lập trình Python", "author": "Nguyễn Văn A", "category": "Công nghệ", "publishedYear": 2024, "status": "available"},
    {"id": 2, "title": "RESTful API", "author": "Trần Văn B", "category": "Công nghệ", "publishedYear": 2023, "status": "borrowed"},
    {"id": 3, "title": "Cơ sở dữ liệu", "author": "Lê Văn C", "category": "Công nghệ", "publishedYear": 2022, "status": "available"},
    {"id": 4, "title": "Toán rời rạc", "author": "Phạm Văn D", "category": "Giáo trình", "publishedYear": 2021, "status": "available"},
    {"id": 5, "title": "Nhập môn AI", "author": "Nguyễn Văn A", "category": "Công nghệ", "publishedYear": 2025, "status": "available"},
    {"id": 6, "title": "Mạng máy tính", "author": "Trần Văn B", "category": "Công nghệ", "publishedYear": 2020, "status": "borrowed"},
    {"id": 7, "title": "Hệ điều hành", "author": "Lê Văn C", "category": "Công nghệ", "publishedYear": 2021, "status": "available"},
    {"id": 8, "title": "Cấu trúc dữ liệu", "author": "Nguyễn Văn A", "category": "Giáo trình", "publishedYear": 2022, "status": "available"},
]

members = [
    {"id": 1, "name": "Trần Thị B", "email": "b@gmail.com", "phone": "0901234567"},
    {"id": 2, "name": "Nguyễn Văn C", "email": "c@gmail.com", "phone": "0912345678"},
]

loans = [
    {"id": 1, "bookId": 2, "memberId": 1, "borrowDate": "2026-03-20", "dueDate": "2026-03-27", "returnDate": None, "status": "borrowing"},
    {"id": 2, "bookId": 5, "memberId": 1, "borrowDate": "2026-03-18", "dueDate": "2026-03-25", "returnDate": None, "status": "borrowing"},
    {"id": 3, "bookId": 1, "memberId": 2, "borrowDate": "2026-03-10", "dueDate": "2026-03-17", "returnDate": "2026-03-16", "status": "returned"},
]


def make_response(data=None, message="Success", metadata=None, status_code=200):
    return jsonify({
        "status": "success" if status_code < 400 else "error",
        "message": message,
        "metadata": metadata,
        "data": data
    }), status_code


@app.route("/books", methods=["GET"])
def get_books():
    search = request.args.get("search", "").strip().lower()
    author = request.args.get("author", "").strip().lower()
    category = request.args.get("category", "").strip().lower()

    filtered_books = books

    if search:
        filtered_books = [
            book for book in filtered_books
            if search in book["title"].lower()
        ]

    if author:
        filtered_books = [
            book for book in filtered_books
            if author in book["author"].lower()
        ]

    if category:
        filtered_books = [
            book for book in filtered_books
            if category in book["category"].lower()
        ]

    return make_response(
        data=filtered_books,
        message="Get books successfully"
    )


@app.route("/books/page-based", methods=["GET"])
def get_books_page_based():
    search = request.args.get("search", "").strip().lower()

    filtered_books = books
    if search:
        filtered_books = [
            book for book in filtered_books
            if search in book["title"].lower()
        ]

    result, metadata = paginate_page_based(filtered_books, request)

    return make_response(
        data=result,
        message="Get books with page-based pagination successfully",
        metadata=metadata
    )


@app.route("/books/offset-limit", methods=["GET"])
def get_books_offset_limit():
    search = request.args.get("search", "").strip().lower()

    filtered_books = books
    if search:
        filtered_books = [
            book for book in filtered_books
            if search in book["title"].lower()
        ]

    result, metadata = paginate_offset_limit(filtered_books, request)

    return make_response(
        data=result,
        message="Get books with offset-limit pagination successfully",
        metadata=metadata
    )


@app.route("/books/cursor", methods=["GET"])
def get_books_cursor():
    search = request.args.get("search", "").strip().lower()

    filtered_books = books
    if search:
        filtered_books = [
            book for book in filtered_books
            if search in book["title"].lower()
        ]

    result, metadata = paginate_cursor(filtered_books, request)

    return make_response(
        data=result,
        message="Get books with cursor pagination successfully",
        metadata=metadata
    )


@app.route("/members", methods=["GET"])
def get_members():
    return make_response(
        data=members,
        message="Get members successfully"
    )


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member_by_id(member_id):
    member = next((m for m in members if m["id"] == member_id), None)

    if not member:
        return make_response(message="Member not found", status_code=404)

    return make_response(
        data=member,
        message="Get member successfully"
    )


@app.route("/loans", methods=["GET"])
def get_loans():
    return make_response(
        data=loans,
        message="Get loans successfully"
    )


@app.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan_by_id(loan_id):
    loan = next((l for l in loans if l["id"] == loan_id), None)

    if not loan:
        return make_response(message="Loan not found", status_code=404)

    return make_response(
        data=loan,
        message="Get loan successfully"
    )


@app.route("/members/<int:member_id>/loans", methods=["GET"])
def get_loans_by_member(member_id):
    member = next((m for m in members if m["id"] == member_id), None)

    if not member:
        return make_response(message="Member not found", status_code=404)

    member_loans = [loan for loan in loans if loan["memberId"] == member_id]

    return make_response(
        data=member_loans,
        message="Get member loans successfully"
    )


if __name__ == "__main__":
    app.run(debug=True)