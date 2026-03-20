# TypeAPI - Library Management API

## Types

### Book
- id: integer
- title: string
- author: string
- published_year: integer

### BookInput
- title: string
- author: string
- published_year: integer

## Endpoints

### GET /books
Response:
- 200 OK -> Book[]

### GET /books/{bookId}
Path Params:
- bookId: integer

Response:
- 200 OK -> Book
- 404 Not Found

### POST /books
Request Body:
- BookInput

Response:
- 201 Created -> Book

### PUT /books/{bookId}
Path Params:
- bookId: integer

Request Body:
- BookInput

Response:
- 200 OK -> Book
- 404 Not Found

### DELETE /books/{bookId}
Path Params:
- bookId: integer

Response:
- 200 OK
- 404 Not Found