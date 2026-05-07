from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/payments', methods=['POST'])
def payment_header_version():

    # Lấy version từ header
    version = request.headers.get('API-Version', '1')

    # ===== Version 1 =====
    if version == '1':

        return jsonify({
            "version": "v1",
            "status": "success"
        })

    # ===== Version 2 =====
    elif version == '2':

        data = request.json

        return jsonify({
            "version": "v2",
            "transactionId": "tx_1001",
            "status": "SUCCESS",
            "amount": data.get("amount"),
            "currency": data.get("currency")
        })

    else:
        return jsonify({
            "error": "Unsupported API version"
        }), 400


if __name__ == '__main__':
    app.run(debug=True)