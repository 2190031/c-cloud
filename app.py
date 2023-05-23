from flask import Flask, render_template, request, redirect, session
from db_models import db, defaultroles, user,  error, sessions
from hash import check_credentials, hash_password
import os, datetime
from createUserFolder import newUserFolder, toStandardName, toNonStandardName
import traceback
import builtins
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
            db.session.add(newuser)
            db.session.commit()
            newUserFolder(username)
            send_mail(email)
            traceback.print_exc()
            return redirect('/login')
        except:
            traceback.print_exc()
            return error
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
                session['user_username'] = toStandardName(username)
                session['user_email'] = email

                print(session.get('user_id'), session.get('user_username'), session.get('user_email'))
                
                return redirect('/dashboard')
            # /{toStandardName(username)}
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
        _username = session.get('user_username')
        path = f'userFiles/{_username}/saved_files'
        files = os.listdir(path)
        
        file_list = []
        for file in files:
            file_dict = {}
            file_dict['name'] = file
            file_dict['creation_time'] = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(path, file))).strftime('%Y-%m-%d %H:%M:%S')
            file_dict['update_time'] = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, file))).strftime('%Y-%m-%d %H:%M:%S')
            file_dict['extension'] = os.path.splitext(file)[1]
            file_list.append(file_dict)

        return render_template('editor.html', user=username, _user=username, files=file_list, id=session.get('user_id'))#

@app.route('/create_file', methods=['POST'])
def create_file():
    username = session.get('user_username') 
    data = request.json
    filename = data['filename']
    extension = '.' + data['extension']
    content = data['content']
    directory = "userFiles/" + username + "/saved_files/"
    filepath = os.path.join(directory, filename + extension )
    print(filepath)

    with builtins.open(filepath, 'w') as f:
        f.write(content)
    return 'File created successfully'


@app.route('/dashboard')
def dashboard():
    
    if 'user_id' not in session:
        return redirect('/login')
    else:
        username = toNonStandardName(session.get('user_username'))
        _username = session.get('user_username')
        title='Dashboard'
        # Ruta a la carpeta donde se encuentran los archivos
        path = f'userFiles/{_username}/saved_files'

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

        return render_template('dashboard.html', title=title, files=file_list, username=username, _username=_username, id=session.get('user_id'))

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        title='Configuración'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        return render_template('settings.html', title=title, username=session.get('user_username'), id=session.get('user_id'), user_info=user_info)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        title='Mi perfil'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        return render_template('profile.html', title=title, username=toNonStandardName(session.get('user_username')), id=session.get('user_id'), user_info=user_info)

@app.route('/profile/profile_picture')
def profile_picture():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        title='Foto de perfil'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        return render_template('settings.html', title=title, username=toNonStandardName(session.get('user_username')), id=session.get('user_id'), user_info=user_info)

@app.route('/load_file', methods=['POST'])
def load_file():
    username = session.get('user_username')
    filename = request.form['filename']
    directory =  "userFiles/" + username + "/saved_files/"
    file_path = os.path.join(directory, filename)

    print(file_path)
    
    if os.path.isfile(file_path):
        try:
            with builtins.open(file_path, 'r') as f:
                lines = f.readlines()
            content = '\n'.join(line for line in lines if not line.isspace())
            return content, filename
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    # Redirect the user to the login page or any other desired location
    return redirect('/login')

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html')

if __name__ == '__main__':
    app.run(debug=True)

