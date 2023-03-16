from flask import Flask, render_template, request, redirect
from db_models import db, role, user, file, historial, version, error, licence, comment, preference, paytransaction, migration, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:c55h32o5n4Mg@localhost/c_cloud'
app.config['SECRET_KEY'] = ""
db.init_app(app)



@app.route('/')
def index():
    title = 'Inicio - C-Cloud'
    return render_template('index.html', title=title) 

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    title = 'Registrarse'

    if request.method == 'POST':
        name     = request.form.get('name')
        surname  = request.form.get('surname')
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')
        usertype = request.form.get('usertype', 1)
        
        newuser = user(name=name, 
                       surname=surname, 
                       username=username, 
                       email=email, 
                       password=password, 
                       usertype=usertype)
        try:
            db.session.add(newuser)
            db.session.commit()
            return redirect('/login')
        except:
            return error
    else:
        return render_template('sign_up.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Iniciar sesión'

    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        
        inserteduser = user.query.filter_by(email=email, password=password).first()

        if inserteduser:
            id = inserteduser.iduser
            newsession = session(id)
            try:
                db.session.add(newsession)
                db.session.commit()
                return redirect('/notfound')
            except:
                return error
        else:
            return redirect('/login')
    else:
        return render_template('login.html', title=title)
    
@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(debug=True)
