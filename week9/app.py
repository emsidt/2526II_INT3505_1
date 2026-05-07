from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# Payment API v1
# =========================

@app.route('/api/v1/payments', methods=['POST'])
def payment_v1():

    response = jsonify({
        "status": "success"
    })

    # Deprecation headers
    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = 'Tue, 01 Dec 2026 00:00:00 GMT'

    return response


# =========================
# Payment API v2
# =========================

@app.route('/api/v2/payments', methods=['POST'])
def payment_v2():

    data = request.json

    response = {
        "transactionId": "tx_1001",
        "status": "SUCCESS",
        "amount": data.get("amount"),
        "currency": data.get("currency"),
        "paymentMethod": data.get("paymentMethod"),
        "customerId": data.get("customerId")
    }

    return jsonify(response)


# =========================
# Home
# =========================

@app.route('/')
def home():
    return "Payment API Running"


# =========================
# Run app
# =========================

if __name__ == '__main__':
    app.run(debug=True)