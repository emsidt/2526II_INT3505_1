# Book Management API - Week 4

A simple Flask-based Book Management API documented with OpenAPI and rendered using Swagger UI.

## Project Overview

This project was developed for **Week 4: API Specification and OpenAPI** in the Service-Oriented Architecture course.

## Deployment

The project was deployed on **Vercel**.

### Live Demo

- Home: https://demo-book-api.vercel.app/
- Swagger UI: https://demo-book-api.vercel.app/docs
- Books Endpoint: https://demo-book-api.vercel.app/books

## Features

The API supports basic book management operations:

- `GET /books` - Get all books
- `POST /books` - Create a new book
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── templates/
│   └── swagger.html
└── public/
    └── openapi.yaml