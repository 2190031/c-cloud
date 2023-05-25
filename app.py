from flask import Flask, render_template, redirect, session

from db_models import db, defaultroles
from render_pages import *
from file_management import load_file, save_file, load_file__blank
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

@app.route('/create_file', methods=['POST'])
def create_file():
    return save_file()

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

