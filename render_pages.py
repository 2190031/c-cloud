import os, datetime

from flask import render_template, session, redirect, request
from sqlalchemy import desc
from db_models import licence, paytransaction, user
from createUserFolder import toNonStandardName, toStandardName
import datetime
import pytz
from babel.dates import format_datetime

def render_index():
    title = 'Inicio - C-Cloud'
    
    return render_template('index.html', title=title) 

def render_login():
    title = 'Iniciar sesión'
    return render_template('login.html', title=title)

def render_licences():
    title = 'Planes - C-Cloud'
    if 'user_id' in session or 'google_id' in session:
        user_id = session.get('user_id')
        last_transaction = paytransaction.query.filter_by(iduser=user_id).order_by(desc(paytransaction.datepaid)).first()
        if last_transaction:
            plan = licence.query.get(last_transaction.idlicence).idlicence
            print(plan)
            return render_template('licences.html', title=title)
        else:
            plan = licence.query.get(3).idlicence
            print(plan)
            return render_template('licences.html', title=title)
    else:
        return render_template('licences.html', title=title)

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
    if 'user_id' in session or 'google_id' in session:
        username = toNonStandardName(session.get('user_username'))
        _username = session.get('user_username')
        title='Dashboard'
        id_licence = session.get('id_licence')
        licence_u = licence.query.get(id_licence)
        # Ruta a la carpeta donde se encuentran los archivos
        path = f'userFiles/{_username}/saved_files'

        # Obtener una lista de todos los archivos en la carpeta
        files = os.listdir(path)

      # Crear una lista de diccionarios para cada archivo
        file_list = []
        for file in files:
            file_dict = {}
            file_dict['name'] = file

            archivo_completo = os.path.join(path, file)
            fecha_creacion_timestamp = os.path.getctime(archivo_completo)
            fecha_creacion = datetime.datetime.fromtimestamp(fecha_creacion_timestamp)
             
            fecha_actualizacion_timestamp = os.path.getmtime(archivo_completo)
            fecha_actualizacion = datetime.datetime.fromtimestamp(fecha_actualizacion_timestamp)

            tz = pytz.timezone('America/Santo_Domingo')
            fecha_creacion_local = fecha_creacion.astimezone(tz)
            fecha_actualizacion_local = fecha_actualizacion.astimezone(tz)

            formato_fecha = "d 'de' MMMM 'de' yyyy 'a las' hh:mm a"
            fecha_creacion_formateada = format_datetime(fecha_creacion_local, formato_fecha, locale='es_DO')
            fecha_actualizacion_formateada = format_datetime(fecha_actualizacion_local, formato_fecha, locale='es_DO')

            file_dict['creation_time'] = fecha_creacion_formateada
            file_dict['update_time'] = fecha_actualizacion_formateada
            file_dict['extension'] = os.path.splitext(file)[1]
            file_list.append(file_dict)

        return render_template('dashboard.html', title=title, files=file_list, username=username, _username=_username, id=session.get('user_id'), licence_u=licence_u)
    else:
        return redirect('/login')

def render_trash_dashboard():
    if 'user_id' in session or 'google_id' in session:
        username = toNonStandardName(session.get('user_username'))
        _username = session.get('user_username')
        title='Archivos eliminados'
        # Ruta a la carpeta donde se encuentran los archivos
        path = f'userFiles/{_username}/saved_files/trash'

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

        return render_template('deleted_files.html', title=title, files=file_list, username=username, _username=_username, id=session.get('user_id'))
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
