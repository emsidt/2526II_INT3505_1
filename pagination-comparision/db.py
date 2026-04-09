import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "library_demo")

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
books = db["books"]


def create_indexes() -> None:
    books.create_index([("book_id", ASCENDING)], unique=True, name="uq_book_id")
    books.create_index(
        [("created_at", DESCENDING), ("_id", DESCENDING)],
        name="idx_created_at_id_desc"
    )
    books.create_index([("author", ASCENDING)], name="idx_author")
    books.create_index([("category", ASCENDING)], name="idx_category")
    books.create_index([("status", ASCENDING)], name="idx_status")