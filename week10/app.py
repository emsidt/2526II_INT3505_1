from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pythonjsonlogger import jsonlogger
import logging
import time
import os

app = Flask(__name__)

# =========================
# Logging với JSON format
# =========================

logger = logging.getLogger("flask_api")
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler("app.log")
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s %(method)s %(path)s %(ip)s %(status_code)s %(response_time)s"
)
log_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.addHandler(console_handler)

# =========================
# Rate Limiting
# =========================

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

# =========================
# Prometheus Metrics
# =========================

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint", "status"]
)

# =========================
# Middleware logging + metrics
# =========================

@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    response_time = time.time() - request.start_time

    endpoint = request.endpoint or "unknown"
    status_code = str(response.status_code)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint,
        status=status_code
    ).observe(response_time)

    logger.info(
        "Incoming request",
        extra={
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr,
            "status_code": response.status_code,
            "response_time": round(response_time, 4)
        }
    )

    return response


# =========================
# Error handler
# =========================

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too many requests",
        "message": "Please try again later"
    }), 429


@app.errorhandler(500)
def internal_error(e):
    logger.error(
        "Internal server error",
        extra={
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr,
            "status_code": 500,
            "response_time": None
        }
    )

    return jsonify({
        "error": "Internal server error"
    }), 500


# =========================
# Health Check
# =========================

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "flask-api",
        "uptime": "running"
    })


# =========================
# Prometheus endpoint
# =========================

@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# =========================
# Demo API endpoints
# =========================

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Mouse"},
    {"id": 3, "name": "Keyboard"}
]


@app.route("/api/products", methods=["GET"])
@limiter.limit("20 per minute")
def get_products():
    return jsonify(products)


@app.route("/api/products/<int:product_id>", methods=["GET"])
@limiter.limit("20 per minute")
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)


@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "123456":
        return jsonify({
            "message": "Login successful",
            "token": "demo-token"
        })

    logger.warning(
        "Failed login attempt",
        extra={
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr,
            "status_code": 401,
            "response_time": None
        }
    )

    return jsonify({
        "error": "Invalid username or password"
    }), 401


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
@limiter.limit("10 per minute")
def delete_product(product_id):
    global products

    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    products = [p for p in products if p["id"] != product_id]

    # Audit log
    logger.info(
        "Audit log: product deleted",
        extra={
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr,
            "status_code": 200,
            "response_time": None,
            "action": "DELETE_PRODUCT",
            "product_id": product_id
        }
    )

    return jsonify({
        "message": "Product deleted successfully",
        "productId": product_id
    })


@app.route("/api/error", methods=["GET"])
def demo_error():
    raise Exception("Demo server error")


# =========================
# Run app
# =========================

if __name__ == "__main__":
    print("DANG CHAY FILE TUAN 10")
    print(app.url_map)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)