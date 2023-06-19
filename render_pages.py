import os
import datetime
import pytz

from flask import render_template, session, redirect, request
from sqlalchemy import desc
from db_models import db, licence, paytransaction, user, error
from createUserFolder import toNonStandardName
from babel.dates import format_datetime
from file_management import get_file_size, actual_licence, check_max_storage, calculate_total_space, storage_per_archive
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

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
        last_transaction = paytransaction.query.filter_by(iduser=user_id).order_by(desc(paytransaction.idpaytransaction)).first()
        if last_transaction:
            id_plan = licence.query.get(last_transaction.idlicence).idlicence
            print(id_plan)
            return render_template('licences.html', title=title, id_plan=id_plan)
        else:
            id_plan = licence.query.get(3).idlicence
            print(id_plan)
            return render_template('licences.html', title=title, id_plan=id_plan)
    else:
        return render_template('licences.html', title=title)

def render_editor():
    if 'user_id' in session or 'google_id' in session:
        id = session.get('user_id')
        o_filename = request.args.get('o_filename')
        username = user.query.filter_by(iduser=id).first()
        _username = session.get('user_username')
        path = f'c-cloud/userFiles/{_username}/saved_files'
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
        role = session.get('user_role')

        title='Dashboard'

        # Ruta a la carpeta donde se encuentran los archivos
        path = f'c-cloud/userFiles/{_username}/saved_files'

        # Obtener una lista de todos los archivos en la carpeta
        files = os.listdir(path)
        total_f = check_max_storage(path)
        total_size_c, unit_c = calculate_total_space(path)
        storage_per_archive_ = storage_per_archive(session.get("user_id"))

        print(total_f)
        # Crear una lista de diccionarios para cada archivo
        total_size = 0.0
        file_size = 0.0
        unit = ""

        file_list = []
        for file in files:
            file_dict = {}
            file_dict['name'] = file

            if file == 'trash' or file == 'old':
                pass
            else:
                file_size, unit = get_file_size(file)
                total_size = total_size + file_size

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
            file_dict['size'] = str(round(file_size, 2)) + unit
            file_list.append(file_dict)

            file_list.sort(key=lambda x: x['update_time'], reverse=True)
            max_storage = actual_licence(session.get("user_id"))

        return render_template('dashboard.html', title=title, files=file_list, username=username, _username=_username, role=role, id=session.get('user_id'), total_space_used=(round(total_size_c, 2)),unit_c=unit_c, max_storage=max_storage, storage_per_archive_=storage_per_archive_)
    else:
        return redirect('/login')


def render_trash_dashboard():
    if 'user_id' in session or 'google_id' in session:
        username = toNonStandardName(session.get('user_username'))
        _username = session.get('user_username')
        title='Archivos eliminados'
        role = session.get('user_role')
        # Ruta a la carpeta donde se encuentran los archivos
        path = f'c-cloud/userFiles/{_username}/saved_files/trash'

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

        return render_template('deleted_files.html', title=title, files=file_list, username=username, _username=_username, role=role, id=session.get('user_id'))
    else:
        return redirect('/login')

def render_settings():
    if 'user_id' in session or 'google_id' in session:
        title='Configuración'
        user_info = user.query.filter_by(iduser=session.get('user_id')).first()

        return render_template('settings.html', title=title, username=session.get('user_username'), id=session.get('user_id'), user_info=user_info)
    else:
        return redirect('/login')

class MyForm(FlaskForm):
    newusername = StringField('Tu nuevo nombre de usuario')
    submit = SubmitField('Confirmar')


def render_profile():
    if 'user_id' in session or 'google_id' in session:
        title='Mi perfil'
        form = MyForm()
        role = session.get('user_role')

        user_info = user.query.filter_by(iduser=session.get('user_id')).first()
        creation_date = user_info.creationdate
        tz = pytz.timezone('America/Santo_Domingo')  # Configura la zona horaria de República Dominicana
        creation_date_local = creation_date.astimezone(tz)
        formatted_date = format_datetime(creation_date_local, "dd 'de' MMMM 'de' yyyy 'a las' hh:mm a", locale='es_DO')
        username_updated = session.pop('username_updated', None)
        username_in_use = session.pop('username_in_use', None)
        return render_template('profile.html', title=title, username=session.get('user_username'), id=session.get('user_id'), role=role, user_info=user_info, formatted_date=formatted_date, username_updated=username_updated,username_in_use=username_in_use, form=form)
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


def render_licence_control():
    title = 'Control de licencias'
    role = session.get('user_role')

    licences = db.session.query(licence).all()
    return render_template('licence_control.html', title=title, role=role, username=session.get('user_username'), licences=licences)

def render_users_control():
    title = 'Control de usuarios'
    role = session.get('user_role')

    users = db.session.query(user).all()
    return render_template('user_control.html', title=title, role=role, username=session.get('user_username'), users=users)

def render_error_reports():
    title = 'Reportes de error'
    role = session.get('user_role')

    reports = db.session.query(error, user.username)\
                .join(user, error.iduser == user.iduser)\
                .order_by(error.is_resolved.asc(), error.datereported.desc())\
                .all()

    report_data = []
    for report, username in reports:
        report_data.append({
            'iderror': report.iderror,
            'username': username,
            'topic': report.topic,
            'description': report.description,
            'datereported': report.datereported,
            'is_resolved': report.is_resolved

            # Agrega aquí los demás atributos que necesites del objeto error
        })

    return render_template('error_reports.html', title=title, role=role, username=session.get('user_username'), reports=report_data)

def render_my_plan():
    if 'user_id' in session or 'google_id' in session:
            id_user = session.get("user_id")
            last_transaction = db.session.query(paytransaction).filter_by(iduser=id_user).order_by(paytransaction.idlicence.desc()).first()
            if last_transaction:
                last_licence_id = last_transaction.idlicence
            else:
                last_licence_id = 3

            title = 'Mi plan'
            role = session.get('user_role')
            new_plan = session.pop("new_plan", None)
            return render_template('my_plan.html', title=title, role=role, username=session.get('user_username'), newplan=new_plan, last_transaction=last_transaction,last_licence_id=last_licence_id )
    else:
        return redirect("/login")



