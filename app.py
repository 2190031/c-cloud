from flask import Flask, render_template, request, redirect, session
from db_models import db, defaultroles, user,  error, sessions
from hash import check_credentials, hash_password
import os, datetime
from createUserFolder import newUserFolder
import traceback
from sendMail import send_mail

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
                       password    =hashed_password,
                       salt        =salt, 
                       usertype    =usertype)
        
        try:
            print(hashed_password)
            send_mail(email)
            db.session.add(newuser)
            db.session.commit()
            newUserFolder(username)
            traceback.print_exc()
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
            username = inserteduser.username
            newsession = sessions(iduser=id)
            try:
                db.session.add(newsession)
                db.session.commit()
                
                session['user_id'] = id
                session['user_username'] = username
                session['user_email'] = email

                return redirect(f'/{username}/dashboard')
            except:
                traceback.print_exc()
                return error
        else:
            return redirect('/login')
    else:
        return render_template('login.html', title=title)

@app.route('/login')
def login_page():
    title = 'Iniciar sesión'
    return render_template('login.html', title=title)

@app.route('/files')
def files():
    return render_template('dashboard.html') # Pantalla de inicio con los archivos del usuario >> userFiles/usuario/saved_files/...

@app.route('/editor')
def editor():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        id = session.get('user_id')
        username = user.query.filter_by(iduser=id).first()
        return render_template('editor.html', user=username)

@app.route('/create_file', methods=['POST'])
def create_file():
    username_dir = 'userFiles/' + session.get('user_username') + '/saved_files'
    print(username_dir)
    data = request.json
    filename = data['filename']
    extension = data['extension']
    content = data['content']
    filepath = os.path.join(str(username_dir), filename + '.' + extension)
    with open(filepath, 'w') as f:
        f.write(content)
    return 'File created successfully'

@app.route('/<string:username>/dashboard')
def dashboard(username):
    if 'user_id' not in session:
        return redirect('/login')
    
    # Ruta a la carpeta donde se encuentran los archivos
    path = f'userFiles/{username}/saved_files'

    # Obtener una lista de todos los archivos en la carpeta
    files = os.listdir(path)

    # Crear una lista de diccionarios para cada archivo
    file_list = []
    for file in files:
        file_dict = {}
        file_dict['name'] = file
        file_dict['creation_time'] = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(path, file))).strftime('%Y-%m-%d %H:%M:%S')
        file_dict['update_time'] = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, file))).strftime('%Y-%m-%d %H:%M:%S')
        file_dict['extension'] = os.path.splitext(file)[1]
        file_list.append(file_dict)

    return render_template('dashboard.html', files=file_list, username=username, id=session.get('user_id'))

@app.route('/<string:username>/settings')
def settings(username):
    if 'user_id' not in session:
        return redirect('/login')
    else:
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        return render_template('settings.html', username=username, id=session.get('user_id'), user_info=user_info)

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(debug=True)

