from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/payments', methods=['POST'])
def payment_media_type():

    accept_header = request.headers.get('Accept')

    # ===== Version 1 =====
    if accept_header == 'application/vnd.myapi.v1+json':

        return jsonify({
            "version": "v1",
            "status": "success"
        })

    # ===== Version 2 =====
    elif accept_header == 'application/vnd.myapi.v2+json':

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
            "error": "Unsupported media type"
        }), 400


if __name__ == '__main__':
    app.run(debug=True)