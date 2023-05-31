from flask import Flask, render_template, redirect, session

from db_models import db, defaultroles
from render_pages import *
from file_management import load_file, create_file, load_file__blank, send_error_report, save_preference
from user_session import login, signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:c55h32o5n4Mg@localhost/c_cloud'
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


@app.route('/dashboard')
def dashboard():
    return render_dashboard()

@app.route('/settings')
def settings():
    return render_settings()

@app.route('/profile')
def profile():
    return render_profile()
    
@app.route('/profile/profile_picture')
def profile_picture():
    return render_profile()

@app.route('/create_file', methods=['POST'])
def create():
    return create_file()

@app.route('/load_file', methods=['POST'])
def open_file():
    return load_file()
    
@app.route('/load_file_blank/<string:file>', methods=['GET'])
def open_file_blank(file):
    return load_file__blank(file)

@app.route('/send_report', methods=['POST'])
def send_report():
    return send_error_report()

@app.route('/save_preferences', methods=['POST'])
def save_pref():
    return save_preference()

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

