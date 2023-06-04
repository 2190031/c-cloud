import os, datetime

from flask import render_template, session, redirect, request

from db_models import user
from createUserFolder import toNonStandardName, toStandardName

def render_index():
    title = 'Inicio - C-Cloud'
    
    return render_template('index.html', title=title) 

def render_login():
    title = 'Iniciar sesión'
    return render_template('login.html', title=title)

def render_editor():
    if 'user_id' in session or 'google_id' in session:
        id = session.get('user_id')
        o_filename = request.args.get('o_filename')
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


        return render_template('editor.html', user=username, _user=username, files=file_list, id=session.get('user_id'), o_filename=o_filename)

def render_dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        return redirect('/login')
        
def render_dashboard():
    if 'user_id' in session or 'google_id' in session:
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
    else:
        return redirect('/login')
  
def render_settings():
    if 'user_id' in session or 'google_id' in session:
        title='Configuración'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        return render_template('settings.html', title=title, username=session.get('user_username'), id=session.get('user_id'), user_info=user_info)
    else:
        return redirect('/login')
       
def render_profile():
    if 'user_id' in session or 'google_id' in session:
        title='Mi perfil'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        print(session.get('user_id'))
        return render_template('profile.html', title=title, username=session.get('user_username'), id=session.get('user_id'), user_info=user_info)
    else:
        return redirect('/login')

def render_profile_picture():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        return redirect('/login')
        
def render_profile_picture():
    if 'user_id' in session or 'google_id' in session:
        title='Foto de perfil'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        return render_template('settings.html', title=title, username=session.get('user_username'), id=session.get('user_id'), user_info=user_info)
    else:
        return redirect('/login')

def render_page():
    title = 'Iniciar sesión'
    return render_template('login.html', title=title)

def render_notfound():
    return render_template('notfound.html')