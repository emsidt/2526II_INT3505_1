# Week 7 - Product Backend API with OpenAPI, FastAPI and MongoDB

## 1. Mục tiêu bài thực hành

Bài thực hành tuần 7 yêu cầu triển khai backend service theo quy trình:

```text
OpenAPI spec → Generate backend code → Connect MongoDB → Implement CRUD → Run server → Test API
```

Resource chính của bài là `Product`.

Các chức năng CRUD cần có:

```text
GET    /products        Lấy danh sách sản phẩm
POST   /products        Thêm sản phẩm mới
GET    /products/{id}   Lấy chi tiết sản phẩm theo id
PUT    /products/{id}   Cập nhật sản phẩm theo id
DELETE /products/{id}   Xoá sản phẩm theo id
```

---

## 2. Cấu trúc thư mục

Sau khi generate code bằng OpenAPI Generator, project có cấu trúc chính như sau:

```text
product-backend-python/
│
├── openapi.yaml
├── requirements.txt
├── pyproject.toml
├── .env
│
└── src/
    └── openapi_server/
        ├── main.py
        ├── db.py
        ├── apis/
        │   ├── default_api.py
        │   └── default_api_base.py
        │
        └── models/
            └── product_input.py
```

Trong đó:

```text
openapi.yaml        File mô tả API
main.py             File tạo FastAPI app
db.py               File kết nối MongoDB
default_api.py      File xử lý các route API thật
models/             Chứa các model được generate từ OpenAPI schema
```

---

## 3. Viết file OpenAPI

Tạo file:

```text
openapi.yaml
```

Nội dung:

```yaml
openapi: 3.0.3

info:
  title: Product API
  version: 1.0.0

servers:
  - url: http://localhost:8000

paths:
  /products:
    get:
      summary: Get all products
      responses:
        "200":
          description: Product list

    post:
      summary: Create product
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ProductInput"
      responses:
        "201":
          description: Product created

  /products/{id}:
    get:
      summary: Get product by id
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Product found
        "404":
          description: Product not found

    put:
      summary: Update product
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ProductInput"
      responses:
        "200":
          description: Product updated
        "404":
          description: Product not found

    delete:
      summary: Delete product
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Product deleted
        "404":
          description: Product not found

components:
  schemas:
    ProductInput:
      type: object
      title: ProductInput
      required:
        - name
        - price
      properties:
        name:
          type: string
          title: name
        price:
          type: number
          title: price
        description:
          type: string
          title: description
        category:
          type: string
          title: category
        stock:
          type: integer
          title: stock
      example:
        name: Laptop Lenovo
        price: 15000000
        description: Laptop for study
        category: Electronics
        stock: 10
```


---

## 4. Generate backend code bằng OpenAPI Generator

Đứng tại thư mục `week7` hoặc thư mục chứa `openapi.yaml`, chạy:

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-fastapi -o product-backend-python
```

Ý nghĩa:

```text
-i openapi.yaml          File OpenAPI đầu vào
-g python-fastapi        Generate backend bằng Python FastAPI
-o product-backend-python Folder output
```

Sau khi generate xong, chuyển vào thư mục backend:

```bash
cd product-backend-python
```

---

## 5. Tạo môi trường ảo Python

Tạo virtual environment:

```bash
python -m venv .venv
```

Kích hoạt venv trên Windows PowerShell:

```bash
.venv\Scripts\activate
```

Nếu dùng Git Bash:

```bash
source .venv/Scripts/activate
```

---

## 6. Cài thư viện cần thiết

Cài các thư viện generated có sẵn:

```bash
pip install -r requirements.txt
```

Cài project ở chế độ editable:

```bash
pip install -e .
```

Cài thư viện kết nối MongoDB:

```bash
pip install motor python-dotenv
```

Trong đó:

```text
motor           MongoDB async driver cho FastAPI
python-dotenv   Đọc biến môi trường từ file .env
```

Nếu thiếu `uvicorn`, cài thêm:

```bash
pip install uvicorn
```

---

## 7. Tạo file cấu hình môi trường

Tạo file:

```text
.env
```

Nội dung:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=product_db
```
Database sử dụng trong bài:

```text
product_db
```

Collection sử dụng:

```text
products
```

---

## 8. Tạo file kết nối MongoDB

Tạo file:

```text
src/openapi_server/db.py
```

Nội dung:

```python
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "product_db")

client = AsyncIOMotorClient(MONGO_URI)

db = client[MONGO_DB]

products_collection = db["products"]
```

File này dùng để tạo kết nối MongoDB và export collection `products_collection` cho các route API sử dụng.

---

## 9. Sửa file xử lý API

Mở file:

```text
src/openapi_server/apis/default_api.py
```

File này là nơi xử lý request thật.

Lưu ý:

```text
default_api_base.py  thường chỉ là base class/interface
default_api.py       mới là file route thật được FastAPI gọi
```

Trong `default_api.py`, thêm các import sau:

```python
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException

from openapi_server.db import products_collection
from openapi_server.models.product_input import ProductInput
```

Thêm hai hàm phụ:

```python
def product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product.get("name"),
        "price": product.get("price"),
        "description": product.get("description"),
        "category": product.get("category"),
        "stock": product.get("stock"),
    }


def to_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid product id")

    return ObjectId(id)
```

---

## 10. Code API: GET all products

Trong `default_api.py`, sửa hàm `products_get`:

```python
@router.get(
    "/products",
    responses={
        200: {"description": "Product list"},
    },
    tags=["default"],
    summary="Get all products",
    response_model_by_alias=True,
)
async def products_get() -> list:
    products = []
    cursor = products_collection.find()

    async for product in cursor:
        products.append(product_serializer(product))

    return products
```

---

## 11. Code API: POST create product

Trong `default_api.py`, sửa hàm `products_post`:

```python
@router.post(
    "/products",
    responses={
        201: {"description": "Product created"},
    },
    tags=["default"],
    summary="Create product",
    response_model_by_alias=True,
)
async def products_post(
    product_input: ProductInput = Body(...),
) -> dict:
    product_data = product_input.model_dump(exclude_none=True)

    result = await products_collection.insert_one(product_data)

    new_product = await products_collection.find_one(
        {"_id": result.inserted_id}
    )

    return product_serializer(new_product)
```

---

## 12. Code API: GET product by id

Trong `default_api.py`, sửa hàm `products_id_get`:

```python
@router.get(
    "/products/{id}",
    responses={
        200: {"description": "Product found"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Get product by id",
    response_model_by_alias=True,
)
async def products_id_get(
    id: str,
) -> dict:
    object_id = to_object_id(id)

    product = await products_collection.find_one(
        {"_id": object_id}
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_serializer(product)
```

---

## 13. Code API: PUT update product

Trong `default_api.py`, sửa hàm `products_id_put`:

```python
@router.put(
    "/products/{id}",
    responses={
        200: {"description": "Product updated"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Update product",
    response_model_by_alias=True,
)
async def products_id_put(
    id: str,
    product_input: ProductInput = Body(...),
) -> dict:
    object_id = to_object_id(id)
    product_data = product_input.model_dump(exclude_none=True)

    result = await products_collection.update_one(
        {"_id": object_id},
        {"$set": product_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await products_collection.find_one(
        {"_id": object_id}
    )

    return product_serializer(updated_product)
```

---

## 14. Code API: DELETE product

Trong `default_api.py`, sửa hàm `products_id_delete`:

```python
@router.delete(
    "/products/{id}",
    responses={
        200: {"description": "Product deleted"},
        404: {"description": "Product not found"},
    },
    tags=["default"],
    summary="Delete product",
    response_model_by_alias=True,
)
async def products_id_delete(
    id: str,
) -> dict:
    object_id = to_object_id(id)

    result = await products_collection.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "message": "Product deleted"
    }
```

---

## 15. Chạy MongoDB

Nếu MongoDB đã cài trên máy, đảm bảo service MongoDB đang chạy.

Kiểm tra bằng MongoDB Compass:

```text
mongodb://localhost:27017
```


Sau khi chạy, MongoDB sẽ lắng nghe tại:

```text
localhost:27017
```

---

## 16. Chạy FastAPI server

Đứng tại thư mục:

```bash
cd "D:/Kiến trúc hướng dịch vụ/2526II_INT3505_1/week7/product-backend-python"
```

Chạy server bằng Uvicorn:

```bash
uvicorn openapi_server.main:app --reload
```

Ý nghĩa lệnh:

```text
uvicorn                    Chương trình chạy server ASGI
openapi_server.main        File main.py trong package openapi_server
app                        Biến FastAPI app trong main.py
--reload                   Tự restart server khi sửa code
```

Khi chạy thành công sẽ thấy:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Mở Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Mở OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

## 17. Test API bằng Swagger UI

Truy cập:

```text
http://127.0.0.1:8000/docs
```

### 17.1. Test POST /products

Body mẫu:

```json
{
  "name": "Laptop Lenovo",
  "price": 15000000,
  "description": "Laptop for study",
  "category": "Electronics",
  "stock": 10
}
```

Kết quả mong muốn:

```json
{
  "id": "690e39757904d025b2598786",
  "name": "Laptop Lenovo",
  "price": 15000000,
  "description": "Laptop for study",
  "category": "Electronics",
  "stock": 10
}
```

Lưu ý `id` là `_id` do MongoDB tự sinh, được convert sang string.

---

### 17.2. Test GET /products

Gọi:

```text
GET /products
```

Kết quả mong muốn:

```json
[
  {
    "id": "690e39757904d025b2598786",
    "name": "Laptop Lenovo",
    "price": 15000000,
    "description": "Laptop for study",
    "category": "Electronics",
    "stock": 10
  }
]
```

---

### 17.3. Test GET /products/{id}

Dùng id đã tạo ở bước POST:

```text
GET /products/690e39757904d025b2598786
```

Kết quả mong muốn:

```json
{
  "id": "690e39757904d025b2598786",
  "name": "Laptop Lenovo",
  "price": 15000000,
  "description": "Laptop for study",
  "category": "Electronics",
  "stock": 10
}
```

---

### 17.4. Test PUT /products/{id}

Request:

```text
PUT /products/690e39757904d025b2598786
```

Body:

```json
{
  "name": "Laptop Lenovo Pro",
  "price": 17000000,
  "description": "Updated laptop",
  "category": "Electronics",
  "stock": 5
}
```

Kết quả mong muốn:

```json
{
  "id": "690e39757904d025b2598786",
  "name": "Laptop Lenovo Pro",
  "price": 17000000,
  "description": "Updated laptop",
  "category": "Electronics",
  "stock": 5
}
```

---

### 17.5. Test DELETE /products/{id}

Request:

```text
DELETE /products/690e39757904d025b2598786
```

Kết quả mong muốn:

```json
{
  "message": "Product deleted"
}
```

---


## 18. Các lệnh terminal tổng hợp

Tạo backend từ OpenAPI:

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-fastapi -o product-backend-python
```

Vào thư mục backend:

```bash
cd product-backend-python
```

Tạo môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt venv PowerShell:

```bash
.venv\Scripts\activate
```

Cài thư viện:

```bash
pip install -r requirements.txt
pip install -e .
pip install motor python-dotenv uvicorn
```

Chạy MongoDB bằng Docker nếu cần:

```bash
docker run -d --name mongodb -p 27017:27017 mongo
```

Chạy server:

```bash
uvicorn openapi_server.main:app --reload
```

Mở Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 20. Kết luận

Bài thực hành đã triển khai được backend service theo quy trình API-first:

```text
1. Viết OpenAPI spec bằng YAML
2. Sinh code backend Python FastAPI bằng OpenAPI Generator
3. Cài thư viện cần thiết
4. Kết nối MongoDB bằng Motor
5. Viết CRUD cho Product
6. Chạy server bằng Uvicorn
7. Test API bằng Swagger UI
```

Backend sau khi hoàn thành có thể lưu dữ liệu thật vào MongoDB và hỗ trợ đầy đủ các chức năng CRUD cho resource `Product`.
