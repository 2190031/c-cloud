from flask import Flask, render_template, request, redirect
from db_models import db, role, user, file, historial, version, error, licence, comment, preference, paytransaction, migration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:c55h32o5n4Mg@localhost/c_cloud'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/sign_up')
def signup():
    title = 'Registrarse'
    return render_template('sign_up.html', title=title)

@app.route('/login')
def login():
    title = 'Iniciar sesión'
    return render_template('login.html', title=title)

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(debug=True)
