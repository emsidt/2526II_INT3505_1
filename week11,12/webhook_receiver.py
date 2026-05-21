from flask import Flask, request, jsonify
import hmac
import hashlib
import json

app = Flask(__name__)

WEBHOOK_SECRET = "my_secret_key"


def verify_signature(payload, received_signature):
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload_json.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, received_signature)


@app.route("/webhook/maintenance", methods=["POST"])
def receive_maintenance_webhook():
    payload = request.get_json()
    received_signature = request.headers.get("X-Webhook-Signature")

    if not received_signature:
        return jsonify({
            "message": "Missing webhook signature"
        }), 400

    is_valid = verify_signature(payload, received_signature)

    if not is_valid:
        return jsonify({
            "message": "Invalid webhook signature"
        }), 401

    print("===== WEBHOOK RECEIVED =====")
    print("Event:", payload.get("event"))
    print("Data:", payload.get("data"))
    print("============================")

    return jsonify({
        "message": "Webhook received successfully"
    }), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Webhook receiver is running"
    })


if __name__ == "__main__":
    app.run(port=6000, debug=True)