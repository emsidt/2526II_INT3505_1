from flask import Flask, request, jsonify
import requests
import hmac
import hashlib
import json
import time
from datetime import datetime

app = Flask(__name__)

# Giả lập database
maintenance_requests = []
webhooks = []

WEBHOOK_SECRET = "my_secret_key"


# =========================
# Helper functions
# =========================

def generate_id(prefix):
    return f"{prefix}_{int(time.time() * 1000)}"


def create_signature(payload):
    """
    Tạo chữ ký HMAC SHA256 để bên nhận webhook xác thực payload.
    """
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)

    signature = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload_json.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature


def dispatch_webhook(event_type, data):
    """
    Gửi webhook đến các URL đã đăng ký theo event_type.
    """
    event_payload = {
        "id": generate_id("evt"),
        "event": event_type,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "data": data
    }

    matched_webhooks = [
        wh for wh in webhooks
        if wh["event"] == event_type and wh["isActive"] is True
    ]

    for wh in matched_webhooks:
        signature = create_signature(event_payload)

        try:
            response = requests.post(
                wh["targetUrl"],
                json=event_payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Webhook-Signature": signature
                },
                timeout=3
            )

            print(f"[WEBHOOK] Sent to {wh['targetUrl']} - Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[WEBHOOK] Failed to send to {wh['targetUrl']}")
            print(str(e))


# =========================
# CRUD PATTERN
# =========================

@app.route("/maintenance-requests", methods=["POST"])
def create_maintenance_request():
    body = request.get_json()

    asset_id = body.get("assetId")
    description = body.get("description")
    priority = body.get("priority", "medium")

    if not asset_id or not description:
        return jsonify({
            "message": "assetId and description are required"
        }), 400

    new_request = {
        "id": generate_id("REQ"),
        "assetId": asset_id,
        "description": description,
        "priority": priority,
        "status": "pending",
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }

    maintenance_requests.append(new_request)

    # Event-driven + Webhook
    dispatch_webhook("maintenance_request.created", new_request)

    return jsonify({
        "message": "Maintenance request created",
        "data": new_request
    }), 201


@app.route("/maintenance-requests", methods=["GET"])
def get_maintenance_requests():
    """
    Query Pattern:
    GET /maintenance-requests?status=pending&priority=high
    """
    status = request.args.get("status")
    priority = request.args.get("priority")

    result = maintenance_requests

    if status:
        result = [item for item in result if item["status"] == status]

    if priority:
        result = [item for item in result if item["priority"] == priority]

    return jsonify({
        "total": len(result),
        "data": result
    }), 200


@app.route("/maintenance-requests/<request_id>", methods=["GET"])
def get_maintenance_request_detail(request_id):
    item = next(
        (req for req in maintenance_requests if req["id"] == request_id),
        None
    )

    if item is None:
        return jsonify({
            "message": "Maintenance request not found"
        }), 404

    return jsonify(item), 200


@app.route("/maintenance-requests/<request_id>", methods=["PATCH"])
def update_maintenance_request(request_id):
    body = request.get_json()

    item = next(
        (req for req in maintenance_requests if req["id"] == request_id),
        None
    )

    if item is None:
        return jsonify({
            "message": "Maintenance request not found"
        }), 404

    allowed_fields = ["description", "priority", "status"]

    for field in allowed_fields:
        if field in body:
            item[field] = body[field]

    # Nếu hoàn thành sửa chữa thì phát event
    if body.get("status") == "completed":
        dispatch_webhook("maintenance_request.completed", item)

    return jsonify({
        "message": "Maintenance request updated",
        "data": item
    }), 200


@app.route("/maintenance-requests/<request_id>", methods=["DELETE"])
def delete_maintenance_request(request_id):
    global maintenance_requests

    item = next(
        (req for req in maintenance_requests if req["id"] == request_id),
        None
    )

    if item is None:
        return jsonify({
            "message": "Maintenance request not found"
        }), 404

    maintenance_requests = [
        req for req in maintenance_requests if req["id"] != request_id
    ]

    return jsonify({
        "message": "Maintenance request deleted"
    }), 200


# =========================
# WEBHOOK PATTERN
# =========================

@app.route("/webhooks", methods=["POST"])
def register_webhook():
    body = request.get_json()

    event = body.get("event")
    target_url = body.get("targetUrl")

    if not event or not target_url:
        return jsonify({
            "message": "event and targetUrl are required"
        }), 400

    webhook = {
        "id": generate_id("WH"),
        "event": event,
        "targetUrl": target_url,
        "isActive": True,
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }

    webhooks.append(webhook)

    return jsonify({
        "message": "Webhook registered",
        "data": webhook
    }), 201


@app.route("/webhooks", methods=["GET"])
def get_webhooks():
    return jsonify({
        "total": len(webhooks),
        "data": webhooks
    }), 200


@app.route("/webhooks/<webhook_id>", methods=["DELETE"])
def delete_webhook(webhook_id):
    global webhooks

    item = next(
        (wh for wh in webhooks if wh["id"] == webhook_id),
        None
    )

    if item is None:
        return jsonify({
            "message": "Webhook not found"
        }), 404

    webhooks = [
        wh for wh in webhooks if wh["id"] != webhook_id
    ]

    return jsonify({
        "message": "Webhook deleted"
    }), 200


@app.route("/webhooks/<webhook_id>/test", methods=["POST"])
def test_webhook(webhook_id):
    item = next(
        (wh for wh in webhooks if wh["id"] == webhook_id),
        None
    )

    if item is None:
        return jsonify({
            "message": "Webhook not found"
        }), 404

    dispatch_webhook(item["event"], {
        "message": "This is a test webhook"
    })

    return jsonify({
        "message": "Test webhook sent"
    }), 200


# =========================
# Health check
# =========================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask API Patterns Demo is running"
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)