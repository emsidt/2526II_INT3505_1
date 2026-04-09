# RAML Demo

## Mục tiêu
Demo file `api.raml` bằng cách chạy mock server từ RAML, sau đó kiểm tra các endpoint bằng trình duyệt, Postman hoặc `curl`.

## Yêu cầu
Cần cài sẵn:
- Node.js
- npm

Kiểm tra phiên bản:

```bash
node -v
npm -v

Cài công cụ mock server:
```bash
npm install -g raml-mocker

Chạy mock server:
raml-mocker -f api.raml -p 5000