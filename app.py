from flask import Flask, render_template, request, redirect
from db_models import db, defaultroles, user,  error, session
from hash import check_credentials, hash_password
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:c55h32o5n4Mg@localhost/c_cloud'
app.config['SECRET_KEY'] = ""
db.init_app(app)

# crifrar el input del login, hacer select de la base de datos,  
# crifrar el resultado, comparar los resultados

with app.app_context():
    db.create_all()
    db.session.commit()
    defaultroles()

@app.route('/')
def index():
    title = 'Inicio - C-Cloud'
    return render_template('index.html', title=title) 
    
@app.route('/a')
def aindex():
    title = 'Inicio - C-Cloud'
    return render_template('aindex.html', title=title) 

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
        
        hashed_password, salt = hash_password(password)

        newuser = user(name        =name, 
                       surname     =surname, 
                       username    =username, 
                       email       =email, 
                       password    =hashed_password.encode('utf-8'),
                       salt        =salt.encode('utf-8'), 
                       usertype    =usertype)
        
        try:
            db.session.add(newuser)
            db.session.commit()
            return redirect('/login')
        except:
            traceback.print_exc()
            return salt.encode('utf-8')
    else:
        return render_template('sign_up.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Iniciar sesión'

    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        
        passwordsMatch = check_credentials(email, password)
        inserteduser = user.query.filter_by(email=email).first()

        if inserteduser and passwordsMatch == True:
            id = inserteduser.iduser
            newsession = session(iduser=id)
            try:
                db.session.add(newsession)
                db.session.commit()
                
                return redirect('/notfound')
            except:
                traceback.print_exc()
                return error
        else:
            return redirect('/login')
    else:
        return render_template('login.html', title=title)
    
@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

# def regSession(iduser):
#     log = session(iduser=iduser)
#     try:
#         db.session.add(log)
#         db.session.commit()
#     except:
#         return "error"

if __name__ == '__main__':
    app.run(debug=True)

