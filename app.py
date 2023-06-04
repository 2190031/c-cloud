import os

from flask import Flask, render_template, redirect, session
from paypal_payments import payment, execute, payment_premium, execute_premium
from user_session import callback, login_google
from db_models import db, defaultlicence, defaultroles
from user_session import login, signup, update_p_data, auth_update
from render_pages import *
from file_management import (load_file, create_file, load_file__blank, send_error_report, save_preference, upload_p_picture, get_profile_pic)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Mauricio2021@localhost/c_cloud"

app.config["SECRET_KEY"] = "secret_key"
app.secret_key = "ODNFAOFNA09q09qpomao989j"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

db.init_app(app)
with app.app_context():
    try:
        db.create_all()
        db.session.commit()
        defaultroles()
        defaultlicence()
    except:
        print("hola")
        
@app.route("/")
def index():
    return render_index()
  

@app.route('/licences')
def planes():
    return render_licences()

@app.route('/payment', methods=['POST'])
def pay():
    return payment()

@app.route('/execute', methods=['POST'])
def execute_pay():
    return execute()

@app.route('/payment/premium', methods=['POST'])
def payment__premium():
    return payment_premium()

@app.route('/execute/premium', methods=['POST'])
def execute_premium_payment():
    return execute_premium()

@app.route("/callback")
def call_back():
    return callback()

@app.route("/signup", methods=["POST", "GET"])

def sign_up():
    return signup()

@app.route("/login", methods=["GET", "POST"])
def log_in():
    return login()

@app.route("/loginG")
def log_in_google():
    return login_google()

@app.route("/login")
def login_page():
    return render_login()

@app.route("/editor")
def editor():
    return render_editor()

@app.route("/create_file", methods=["POST"])
def create_files():
    return create_file()

@app.route("/dashboard")
def dashboard():
    return render_dashboard()

@app.route("/settings")
def settings():
    return render_settings()

@app.route("/profile")
def profile():
    return render_profile()

@app.route("/profile/profile_picture")
def profile_picture():
    return render_profile_picture()

@app.route("/create_file", methods=["POST"])
def create():
    return create_file()

@app.route("/load_file", methods=["POST"])
def open_file():
    return load_file()

@app.route("/load_file_blank/<string:file>", methods=["GET"])
def open_file_blank(file):
    return load_file__blank(file)

@app.route("/send_report", methods=["POST"])
def send_report():
    return send_error_report()

@app.route("/save_preferences", methods=["POST"])
def save_pref():
    return save_preference()

@app.route("/upload_profile_picture", methods=["POST"])
def upload_profile_picture():
    return upload_p_picture()

@app.route("/update_profile_data", methods=["POST"])
def update_profile_data():
    return update_p_data()

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/notfound")
def notfound():
    return render_notfound()

@app.route("/auth_update", methods=["POST"])
def auth():
    return auth_update()

@app.route('/get_profile_pic', methods=['GET'])
def profile_photo():
    return get_profile_pic()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html")

if __name__ == "__main__":
    app.run(debug=True)