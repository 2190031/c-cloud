import paypalrestsdk

from flask import jsonify, request

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AdvcMAZRch_a2_IX8HcOahjLOrd0PGTh4sjj_Fq6UdgrVUsf38Gwttt04IVoCR5hc0nKcONkEGXjtghB",
    "client_secret": "EM2-afNHVKHKLSoFtoDKbQ4Ap1U3VTmaXiXT3-8CwOILetphM5qt_KwEy8244739kZSDGJddmbcGZ5ar"
})

def payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/execute",
            "cancel_url": "http://127.0.0.1:5000/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Plan Básico",
                    "sku": "BASICO",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }]
    })

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID':payment.id})

def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id':request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success':success})

def payment_premium():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/execute/premium",
            "cancel_url": "http://127.0.0.1:5000/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Plan Premium",
                    "sku": "PREMIUM",
                    "price": "20.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "20.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }]
    })

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID':payment.id})

def execute_premium():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id':request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

        return jsonify({'success':success})