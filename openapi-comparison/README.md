# API Documentation Format Comparison

This folder compares 5 API description styles for a simple Library Management API:

- OpenAPI
- API Blueprint
- RAML
- TypeSpec
- TypeAPI

## Demo API
The sample API manages books in a library:

- GET /books
- GET /books/{bookId}
- POST /books
- PUT /books/{bookId}
- DELETE /books/{bookId}

## Goal
- Compare readability and structure
- Compare documentation-first vs type-first styles
- Demonstrate code/test generation where supported

## Folder Structure

- `0_OpenAPI`: OpenAPI YAML specification
- `1_APIBlueprint`: API Blueprint documentation
- `2_RAML`: RAML API specification
- `3_TypeSpec`: TypeSpec source and OpenAPI emission setup
- `4_TypeAPI`: simple type-first custom API description

##  Demo sinh code/test từ file tài liệu

### Sinh code
**OpenAPI** là format mạnh nhất để demo codegen, vì OpenAPI Generator hỗ trợ rất nhiều generator cho client/server/doc. :contentReference[oaicite:7]{index=7}

Ví dụ:

```bash
openapi-generator-cli generate -i OpenAPI/openapi.yaml -g python-flask -o generated-flask-server
openapi-generator-cli generate -i OpenAPI/openapi.yaml -g typescript-fetch -o generated-ts-client