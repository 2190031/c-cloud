from flask import Flask, render_template, redirect, session
from flask import Flask, render_template, jsonify, request
from db_models import db, defaultroles
from render_pages import *
from file_management import load_file, create_file, load_file__blank
from user_session import login, signup
import paypalrestsdk

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mauricio2021@localhost/c_cloud'
app.config['SECRET_KEY'] = "secret_key"

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        db.session.commit()
        defaultroles()
    except:
        print('error')

@app.route('/')
def index():
    return render_index()
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AdvcMAZRch_a2_IX8HcOahjLOrd0PGTh4sjj_Fq6UdgrVUsf38Gwttt04IVoCR5hc0nKcONkEGXjtghB",
    "client_secret": "EM2-afNHVKHKLSoFtoDKbQ4Ap1U3VTmaXiXT3-8CwOILetphM5qt_KwEy8244739kZSDGJddmbcGZ5ar"
})

@app.route('/planes')
def planes():
    return render_template('planes.html')

@app.route('/payment', methods=['POST'])
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

    return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success': success})


@app.route('/payment/premium', methods=['POST'])
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

    return jsonify({'paymentID': payment.id})


@app.route('/execute/premium', methods=['POST'])
def execute_premium():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success': success})


if __name__ == '__main__':
    app.run(debug=True)


    
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    return signup()

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    return login()
    
@app.route('/login')
def login_page():
    return render_login()

@app.route('/editor')
def editor():
    return render_editor()

@app.route('/create_file', methods=['POST'])
def create_file():
    return create_file()

@app.route('/dashboard')
def dashboard():
    return render_dashboard()

@app.route('/settings')
def settings():
    return render_settings()

@app.route('/profile')
def profile():
    render_profile()
    
@app.route('/profile/profile_picture')
def profile_picture():
    return render_profile()

@app.route('/load_file', methods=['POST'])
def open_file():
    return load_file()
    
@app.route('/load_file_blank', methods=['POST'])
def open_file_blank():
    return load_file__blank()

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/notfound')
def notfound():
    return render_notfound()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')



if __name__ == '__main__':
    app.run(debug=True)

