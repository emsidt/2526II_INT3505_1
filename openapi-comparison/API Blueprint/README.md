# API Blueprint Demo

## Mục tiêu
Demo file `api.apib` bằng cách chạy mock server từ API Blueprint, sau đó test các endpoint bằng trình duyệt hoặc Postman.

## Yêu cầu
Cần cài sẵn:
- Node.js
- npma

Kiểm tra:

```bash
node -v
npm -v

Cài công cụ mock server:

npm install -g drakov

Chạy mock server:

drakov -f api.apib -p 5000


# API Blueprint to OpenAPI to Code Generation

## Mục tiêu
Chuyển file `api.apib` từ API Blueprint sang OpenAPI, sau đó dùng OpenAPI Generator để sinh code.

Cách này dễ thực hiện hơn so với việc sinh code trực tiếp từ API Blueprint, vì hệ sinh thái code generation của OpenAPI mạnh và phổ biến hơn nhiều.

## Quy trình
Thực hiện theo luồng:

```text
api.apib -> OpenAPI (JSON/YAML) -> generated code / server stub

Cài công cụ chuyển API Blueprint sang OpenAPI
npm install -g apib2swagger

Chuyển api.apib sang OpenAPI
npx apib2swagger -i api.apib --open-api-3 -o openapi.json

Sinh code:
npx @openapitools/openapi-generator-cli generate -i openapi.json -g spring -o generated-spring