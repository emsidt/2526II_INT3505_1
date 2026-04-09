import base64
import os
import time
from datetime import datetime
from typing import Any, Dict, Tuple

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import DESCENDING

from db import books, create_indexes

load_dotenv()

app = Flask(__name__)
create_indexes()


def make_response(data=None, message="Success", metadata=None, status_code=200):
    return jsonify(
        {
            "status": "success" if status_code < 400 else "error",
            "message": message,
            "metadata": metadata,
            "data": data,
        }
    ), status_code


def serialize_book(doc: dict) -> dict:
    created_at = doc.get("created_at")
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()

    return {
        "id": str(doc["_id"]),
        "book_id": doc["book_id"],
        "title": doc["title"],
        "author": doc["author"],
        "category": doc["category"],
        "publishedYear": doc["publishedYear"],
        "status": doc["status"],
        "isbn": doc["isbn"],
        "created_at": created_at,
    }


def build_filter(args) -> Dict[str, Any]:
    query: Dict[str, Any] = {}

    author = args.get("author", "").strip()
    category = args.get("category", "").strip()
    status = args.get("status", "").strip()
    keyword = args.get("search", "").strip()

    if author:
        query["author"] = author
    if category:
        query["category"] = category
    if status:
        query["status"] = status
    if keyword:
        query["title"] = {"$regex": keyword, "$options": "i"}

    return query


def encode_cursor(created_at: datetime, oid: ObjectId) -> str:
    raw = f"{created_at.isoformat()}|{str(oid)}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_cursor(token: str) -> Tuple[datetime, ObjectId]:
    raw = base64.urlsafe_b64decode(token.encode()).decode()
    created_at_str, oid_str = raw.split("|")
    return datetime.fromisoformat(created_at_str), ObjectId(oid_str)


@app.get("/health")
def health():
    return make_response(
        message="OK",
        data={"count": books.count_documents({})}
    )


@app.get("/books/page-based")
def get_books_page_based():
    query = build_filter(request.args)
    page = max(int(request.args.get("page", 1)), 1)
    size = max(min(int(request.args.get("size", 20)), 100), 1)
    skip = (page - 1) * size

    t0 = time.perf_counter()
    cursor = books.find(query).sort("created_at", DESCENDING).skip(skip).limit(size)
    items = [serialize_book(doc) for doc in cursor]
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    total = books.count_documents(query)
    has_next = skip + size < total

    return make_response(
        data=items,
        message="Get books with page-based pagination successfully",
        metadata={
            "page": page,
            "size": size,
            "skip": skip,
            "total": total,
            "has_next": has_next,
            "elapsed_ms": elapsed_ms,
            "note": "Page-based trong MongoDB thường vẫn dùng skip/limit nên khi page sâu sẽ chậm dần.",
        },
    )


@app.get("/books/offset-limit")
def get_books_offset_limit():
    query = build_filter(request.args)
    offset = max(int(request.args.get("offset", 0)), 0)
    limit = max(min(int(request.args.get("limit", 20)), 100), 1)

    t0 = time.perf_counter()
    cursor = books.find(query).sort("created_at", DESCENDING).skip(offset).limit(limit)
    items = [serialize_book(doc) for doc in cursor]
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    explain = books.find(query).sort("created_at", DESCENDING).skip(offset).limit(limit).explain()
    stats = explain.get("executionStats", {})

    return make_response(
        data=items,
        message="Get books with offset-limit pagination successfully",
        metadata={
            "offset": offset,
            "limit": limit,
            "elapsed_ms": elapsed_ms,
            "executionTimeMillis": stats.get("executionTimeMillis"),
            "totalDocsExamined": stats.get("totalDocsExamined"),
            "totalKeysExamined": stats.get("totalKeysExamined"),
        },
    )


@app.get("/books/cursor")
def get_books_cursor():
    base_query = build_filter(request.args)
    limit = max(min(int(request.args.get("limit", 20)), 100), 1)
    cursor_token = request.args.get("cursor")

    query = dict(base_query)

    if cursor_token:
        created_at, oid = decode_cursor(cursor_token)
        query["$or"] = [
            {"created_at": {"$lt": created_at}},
            {"created_at": created_at, "_id": {"$lt": oid}},
        ]

    t0 = time.perf_counter()
    docs = list(
        books.find(query)
        .sort([("created_at", DESCENDING), ("_id", DESCENDING)])
        .limit(limit + 1)
    )
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    has_next = len(docs) > limit
    docs = docs[:limit]

    next_cursor = None
    if has_next and docs:
        last = docs[-1]
        next_cursor = encode_cursor(last["created_at"], last["_id"])

    explain = (
        books.find(query)
        .sort([("created_at", DESCENDING), ("_id", DESCENDING)])
        .limit(limit)
        .explain()
    )
    stats = explain.get("executionStats", {})

    return make_response(
        data=[serialize_book(doc) for doc in docs],
        message="Get books with cursor pagination successfully",
        metadata={
            "limit": limit,
            "next_cursor": next_cursor,
            "has_next": has_next,
            "elapsed_ms": elapsed_ms,
            "executionTimeMillis": stats.get("executionTimeMillis"),
            "totalDocsExamined": stats.get("totalDocsExamined"),
            "totalKeysExamined": stats.get("totalKeysExamined"),
        },
    )


@app.get("/benchmark/explain")
def benchmark_explain():
    offset = max(int(request.args.get("offset", 500000)), 0)
    limit = max(min(int(request.args.get("limit", 20)), 100), 1)

    offset_explain = (
        books.find({})
        .sort("created_at", DESCENDING)
        .skip(offset)
        .limit(limit)
        .explain()
    )

    anchor_docs = list(
        books.find({})
        .sort([("created_at", DESCENDING), ("_id", DESCENDING)])
        .skip(offset)
        .limit(1)
    )

    if not anchor_docs:
        return make_response(message="No data", status_code=404)

    anchor = anchor_docs[0]

    cursor_query = {
        "$or": [
            {"created_at": {"$lt": anchor["created_at"]}},
            {"created_at": anchor["created_at"], "_id": {"$lt": anchor["_id"]}},
        ]
    }

    cursor_explain = (
        books.find(cursor_query)
        .sort([("created_at", DESCENDING), ("_id", DESCENDING)])
        .limit(limit)
        .explain()
    )

    return make_response(
        data={
            "offset_limit": offset_explain.get("executionStats", {}),
            "cursor": cursor_explain.get("executionStats", {}),
        },
        message="Explain benchmark generated successfully",
        metadata={"offset": offset, "limit": limit},
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)