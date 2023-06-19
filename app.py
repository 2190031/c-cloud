import os
import datetime
from flask import Flask, redirect, session, jsonify, request
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from db_models import db, defaultlicence, defaultroles
from user_session import callback, login_google, login, signup, update_p_data, auth_update, deactivate_account, update_p_data_google, control_deactivate_user, control_reactivate_user, control_update_user, control_update_licence
from render_pages import render_dashboard, render_editor, render_index, render_licences, render_login, render_notfound, render_profile, render_profile_picture, render_template, render_trash_dashboard, render_licence_control, render_users_control, render_error_reports, render_my_plan
from file_management import load_file, create_file, load_file__blank, send_error_report, mark_as_resolved, save_preference, upload_p_picture, get_profile_pic, delete_file, download_file, permanently_delete, restore_file, move_to_trash, upload_file
from paypal_payments import payment_basic, execute_basic, payment_premium, execute_premium, mail


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://wady01:copernicus1546@wady01.mysql.pythonanywhere-services.com/wady01$c_cloud"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,  # Tiempo en segundos antes de reciclar las conexiones
}
app.config["SECRET_KEY"] = "secret_key"
app.secret_key = "ODNFAOFNA09q09qpomao989j"
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'c_cloud2023@outlook.com'
app.config['MAIL_PASSWORD'] = 'C-cloud2023'

mail.init_app(app)

csrf = CSRFProtect(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

db.init_app(app)
with app.app_context():
    try:
        db.connect()
        db.create_all()
        db.session.commit()
        defaultroles()
        defaultlicence()
    except:
        print("")

@app.route("/")
def index():
    return render_index()

@app.route('/licences')
def planes():
    return render_licences()

@csrf.exempt
@app.route('/payment/basic', methods=['POST'])
def pay():
    return payment_basic()

@csrf.exempt
@app.route('/upload_file', methods=['POST'])
def upload_file_():
    return upload_file()

@csrf.exempt
@app.route('/execute/basic', methods=['POST'])
def execute_pay():
    return execute_basic()

@csrf.exempt
@app.route('/payment/premium', methods=['POST'])
def payment__premium():
    return payment_premium()

@csrf.exempt
@app.route('/execute/premium', methods=['POST'])
def execute_premium_payment():
    return execute_premium()

@app.route("/callback")
def call_back():
    return callback()

@csrf.exempt
@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    return signup()

@csrf.exempt
@app.route("/login", methods=["GET", "POST"])
def log_in():
    return login()

@app.route("/loginG")
def log_in_google():
    return login_google()

@csrf.exempt
@app.route("/login")
def login_page():
    return render_login()

@app.route("/editor")
def editor():
    return render_editor()

@csrf.exempt
@app.route("/create_file", methods=["POST"])
def create_files():
    return create_file()

@csrf.exempt
@app.route("/download_file", methods=["POST"])
def download():
    return download_file()

@csrf.exempt
@app.route('/guardar_zona_horaria', methods=['GET'])
def guardar_zona_horaria():
    zona_horaria = request.args.get('zona_horaria')
    session.pop("zona_horaria", None)
    session["zona_horaria"] = zona_horaria
    return session.get("zona_horaria")


@app.route("/dashboard")
def dashboard():
    return render_dashboard()

@app.route("/deleted_files")
def deleted_files():
    return render_trash_dashboard()

@app.route("/profile")
def profile():
    return render_profile()

@app.route("/profile/profile_picture")
def profile_picture():
    return render_profile_picture()

@csrf.exempt
@app.route("/create_file", methods=["POST"])
def create():
    return create_file()

@csrf.exempt
@app.route("/delete_file", methods=["POST"])
def delete():
    return delete_file()

@csrf.exempt
@app.route("/move_to_trash", methods=["POST"])
def to_trash():
    return jsonify(move_to_trash())

@csrf.exempt
@app.route("/perm_delete", methods=["POST"])
def perm_delete():
    return permanently_delete()

@csrf.exempt
@app.route("/restore_file", methods=["POST"])
def rest_file():
    return jsonify(restore_file())

@csrf.exempt
@app.route("/load_file", methods=["POST"])
def open_file():
    return load_file()

@csrf.exempt
@app.route("/load_file_blank/<string:file>", methods=["GET"])
def open_file_blank(file):
    return load_file__blank(file)

@csrf.exempt
@app.route("/send_report", methods=["POST"])
def send_report():
    return send_error_report()

@csrf.exempt
@app.route("/save_preferences", methods=["POST"])
def save_pref():
    return save_preference()

@csrf.exempt
@app.route("/upload_profile_picture", methods=["POST"])
def upload_profile_picture():
    return upload_p_picture()

@csrf.exempt
@app.route("/update_profile_data", methods=["POST"])
def update_profile_data():
    return update_p_data()

@csrf.exempt
@app.route("/update_profile_data_google", methods=["POST"])
def update_profile_data_google():
    return update_p_data_google()

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/notfound")
def notfound():
    return render_notfound()

@csrf.exempt
@app.route("/auth_update", methods=["POST"])
def auth():
    return auth_update()

@csrf.exempt
@app.route("/auth_deactivate", methods=["POST"])
def deact_account():
    return deactivate_account()

@csrf.exempt
@app.route('/get_profile_pic', methods=['GET'])
def profile_photo():
    return get_profile_pic()

@app.route('/licence_control')
def licence_control():
    return render_licence_control()

@app.route('/user_control')
def user_control():
    return render_users_control()

@app.route('/error_reports')
def error_reports():
    return render_error_reports()

@csrf.exempt
@app.route('/mark_as_resolved', methods=['POST'])
def mark():
    return mark_as_resolved()

@csrf.exempt
@app.route('/control_deactivate_user', methods=['POST'])
def control_deactivate():
    return control_deactivate_user()

@csrf.exempt
@app.route('/control_reactivate_user', methods=['POST'])
def control_reactivate():
    return control_reactivate_user()

@csrf.exempt
@app.route('/control_update_user', methods=['POST'])
def control_update():
    return control_update_user()

@csrf.exempt
@app.route('/control_update_licence', methods=['POST'])
def control_update_lic():
    return control_update_licence()

@app.route('/my_plan')
def plan():
    return render_my_plan()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html")

if __name__ == "__main__":
    app.run(debug=True)