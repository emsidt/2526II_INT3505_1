# OpenAPI Demo

## Run documentation
You can open this file in Swagger Editor or Swagger UI.

## Generate code
Using OpenAPI Generator:

```bash
openapi-generator-cli generate -i openapi.yaml -g python-flask -o generated-server
openapi-generator-cli generate -i openapi.yaml -g javascript -o generated-js-client