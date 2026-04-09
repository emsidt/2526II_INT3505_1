import random
import string
import time
from datetime import datetime, timedelta

from faker import Faker

from db import books, create_indexes

fake = Faker("vi_VN")
random.seed(42)
Faker.seed(42)

CATEGORIES = ["Công nghệ", "Giáo trình", "Khoa học", "Kinh tế", "Văn học"]
STATUSES = ["available", "borrowed", "reserved"]
AUTHORS = [
    "Nguyễn Văn A", "Trần Văn B", "Lê Văn C", "Phạm Văn D", "Hoàng Văn E",
    "Vũ Thị F", "Đỗ Minh G", "Bùi Lan H", "Ngô Quốc I", "Đặng Thu J"
]
ADJECTIVES = [
    "Hiện đại", "Nâng cao", "Thực hành", "Cơ bản", "Chuyên sâu",
    "Ứng dụng", "Tối ưu", "Phân tán", "Thông minh", "Tự động"
]
SUBJECTS = [
    "Python", "Java", "REST API", "MongoDB", "Thuật toán",
    "Cơ sở dữ liệu", "Hệ điều hành", "Mạng máy tính", "AI", "Cloud"
]


def random_title() -> str:
    return f"{random.choice(SUBJECTS)} {random.choice(ADJECTIVES)} {random.randint(1, 999999)}"


def generate_book(i: int, base_time: datetime) -> dict:
    created_at = base_time - timedelta(seconds=i)
    return {
        "book_id": i,
        "title": random_title(),
        "author": random.choice(AUTHORS),
        "category": random.choice(CATEGORIES),
        "publishedYear": random.randint(2015, 2026),
        "status": random.choice(STATUSES),
        "isbn": "".join(random.choices(string.digits, k=13)),
        "created_at": created_at,
    }


def seed(total: int = 1_000_000, batch_size: int = 10000) -> None:
    books.drop()
    create_indexes()

    base_time = datetime.utcnow()
    docs = []
    start = time.perf_counter()

    for i in range(1, total + 1):
        docs.append(generate_book(i, base_time))

        if len(docs) == batch_size:
            books.insert_many(docs, ordered=False)
            docs.clear()

            if i % (batch_size * 5) == 0:
                elapsed = time.perf_counter() - start
                print(f"Inserted {i:,}/{total:,} docs in {elapsed:.2f}s")

    if docs:
        books.insert_many(docs, ordered=False)

    elapsed = time.perf_counter() - start
    print(f"Done. Inserted {total:,} docs in {elapsed:.2f}s")


if __name__ == "__main__":
    seed()