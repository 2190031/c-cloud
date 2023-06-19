import traceback, hashlib, logging, secrets, os, pathlib, google, requests, cachecontrol, shutil, sys
sys.path.append('c-cloud/venv')
from flask import render_template, request, redirect, session, jsonify, abort

from sqlalchemy import desc, update
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from db_models import db, licence, paytransaction, user, error, sessions
from hash import hash_password, check_credentials
from createUserFolder import newUserFolder, toStandardName
from sendMail import send_mail, account_deactivated_user_mail, account_deactivated_admin_mail, password_changed_mail
from flask_wtf import FlaskForm
from wtforms import SubmitField
from paypal_payments import enviar_bienvenida

# configuracion del cliente de google
GOOGLE_CLIENT_ID = (
    "621438977816-o6ee2tto4rgsk9isrvpv6mm1ctvnkagb.apps.googleusercontent.com"
)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="https://wady01.pythonanywhere.com/callback",
)

def callback():
        flow.fetch_token(authorization_response=request.url)
        if "state" in session:
            if not session["state"] == request.args["state"]:
                abort(500)

            credentials = flow.credentials
            request_session = requests.Session()
            cached_session = cachecontrol.CacheControl(request_session)
            token_request = google.auth.transport.requests.Request(session=cached_session)

            id_info = id_token.verify_oauth2_token(
                id_token=credentials._id_token,
                request=token_request,
                audience=GOOGLE_CLIENT_ID,
            )

            googleid = id_info.get("sub")
            google_name = id_info.get("name")
            google_email = id_info.get("email")
            google_picture = id_info.get("picture")
            if "family_name" in id_info:
                google_family_name = id_info["family_name"]
            else:
                google_family_name = None

            google_username = google_email.split("@")[0]
            google_user_verify = user.query.filter_by(google_id=googleid).first()

            if google_user_verify:
                session.clear()
                id = google_user_verify.iduser
                role = google_user_verify.usertype
                newsession = sessions(iduser=id)
                try:
                    db.session.add(newsession)
                    db.session.commit()

                    _iduser = user.query.filter_by(google_id=googleid).first()

                    session["user_id"] = _iduser.iduser
                    session["user_name"] = google_name
                    session["user_email"] = id_info.get("email")
                    session["google_picture"] = id_info.get("picture")
                    session["user_username"] = google_user_verify.username
                    session["user_role"] = role

                    user_id_licence = session.get('user_id')

                    last_transaction = paytransaction.query.filter_by(iduser=user_id_licence).order_by(
                        desc(paytransaction.datepaid)).first()
                    if last_transaction:
                        plan = licence.query.get(last_transaction.idlicence).idlicence
                        session["id_licence_user"] = plan
                    else:
                        plan = licence.query.get(3).idlicence
                        session["id_licence_user"] = plan

                    return redirect("/")
                except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})
            else:
                google_verify = user.query.filter_by(email=google_email).first()
            if google_verify:
                session["error"] = "El correo está registrado con contraseña. Por favor, ingrese los credenciales"
                return redirect("/login")
            else:
                new_user = user(
                    google_id=googleid,
                    name=google_name,
                    username=google_username,
                    surname=google_family_name,
                    password=None,
                    salt=None,
                    email=google_email,
                    picture=google_picture,
                    usertype=1,
                )
                db.session.add(new_user)
                db.session.commit()
                newUserFolder(google_username)
                enviar_bienvenida(google_username, google_email, google_name)
                session["success"] = "Inicie sesión nuevamente"
                return redirect("/")
        else:
            return redirect("/")

def login_google():
    if "google_id" in session or "user_id" in session:
        return redirect("/")
    else:
        state = secrets.token_urlsafe(16)  # Generar un valor único para 'state'
        session["state"] = state
        authorization_url, _ = flow.authorization_url(
            prompt="select_account", state=state
        )
        return redirect(authorization_url)

class MyForm(FlaskForm):
    submit = SubmitField('Confirmar')

def signup():
    title = 'Registrarse'
    form = MyForm()

    if "google_id" in session or "user_id" in session:
        # si se ha iniciado sesion redirije a index.html
       return redirect("/")
    else:
        if request.method == 'POST':
            # toma los valores enviados por el formulario
            name = request.form.get('name')
            surname = request.form.get('surname')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            usertype = request.form.get('usertype', 1)
            path = f'c-cloud/userFiles/{username}/acc_settings/profile_pic/profile_pic.png'

            #verifica si el correo que se va a registrar ya existe
            verify_email = user.query.filter_by(email=email).first()
            if verify_email:
                session["error"] = "El correo que proporcionaste está registrado. Debe iniciar sesión si quiere acceder con él."
                return redirect("/signup")
            else:
                # cifra la contraseña y la almacena junto a la sal en variables
                hashed_password, salt = hash_password(password)

                # prepara el insert a la base de datos
                newuser = user( name      = name,
                                surname   = surname,
                                username  = username,
                                email     = email,
                                password  = hashed_password,
                                salt      = salt,
                                picture   = path,
                                usertype  = usertype,
                                is_active = True)
                try:
                    # realiza el insert en la base de datos
                    db.session.add(newuser)
                    db.session.commit()

                    #crea los directorios para el usuario
                    newUserFolder(username)

                    enviar_bienvenida(username, email, name)
                    session["success"] = "Inicie sesión nuevamente"
                    return redirect('/login')
                except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})
        else:
            success_message = session.pop("success", None)
            error_message = session.pop("error", None)
            return render_template('sign_up.html', title=title, success_message=success_message, error_message=error_message, form=form)

class MyFormLogin(FlaskForm):
    submit = SubmitField('Confirmar')

def login():
    form = MyFormLogin()
    if "user_id" in session:
        # si la sesion esta iniciada regresa al index
        return redirect('/')
    else:
        title = 'Iniciar sesión'
        if request.method == 'POST':
            # toma los valores del formulario
            email = request.form.get('email')
            password = request.form.get('password')

            # verifica las credenciales del usuario
            passwordsMatch = check_credentials(email, password)
            inserteduser = user.query.filter_by(email=email).first()

            # si el usuario existe, las contraseñas coinciden, y está activo inicia sesion
            if inserteduser is not None and inserteduser.is_active == True and passwordsMatch == True:
                # toma los datos del usuario de la base de datos y crea una cookie
                id = inserteduser.iduser
                name = inserteduser.name
                username = inserteduser.username
                # registra la sesion en la base de datos
                newsession = sessions(iduser=id)
                role = inserteduser.usertype
                try:
                    db.session.add(newsession)
                    db.session.commit()

                    session['user_id'] = id
                    session['user_username'] = toStandardName(username)
                    session['user_email'] = email
                    session['user_name'] = name
                    session["user_role"] = role

                    user_id_licence = session.get('user_id')

                    last_transaction = paytransaction.query.filter_by(iduser=user_id_licence).order_by(desc(paytransaction.datepaid)).first()
                    if last_transaction:
                        # si el usuario ha comprado un plan (el mas reciente comprado) se agrega a la cookie
                        plan = licence.query.get(last_transaction.idlicence).idlicence
                        session["id_licence_user"] = plan
                    else:
                        # si no ha comprado un plan se le asigna el gratuito
                        plan = licence.query.get(3).idlicence
                        session["id_licence_user"] = plan
                    return redirect('/dashboard')
                except:
                    traceback.print_exc()
                    return error
            elif inserteduser is not None and inserteduser.is_active == False:
                session["error"] = "Parece que esta cuenta ha sido eliminada o desactivada."
                return redirect('/login')
            else:
                session["error"] = "Credenciales incorrectas."
                return redirect('/login')
        else:
            success_message = session.pop("success", None)
            error_message = session.pop("error", None)
            return render_template('login.html', title=title, error_message=error_message, success_message=success_message, form=form)

def update_p_data_google():
    idu = session.get('user_id')
    update_user = session['user_username']
    update_new_user = request.form.get('newusername')

    # Verificar si el nombre de usuario ya existe en la base de datos
    existing_user = user.query.filter_by(username=update_new_user).first()
    if existing_user:
        session["username_in_use"] = "Usuario en uso"
        return redirect('/profile')
    else:
        try:
            # Actualizar el nombre de usuario en la base de datos
            update_query = update(user).where(user.iduser == idu).values(username=update_new_user)
            db.session.execute(update_query)
            db.session.commit()

            # Renombrar la carpeta de archivos con el nuevo nombre de usuario
            old_path = f'c-cloud/userFiles/{update_user}'
            new_path = f'c-cloud/userFiles/{update_new_user}'
            os.rename(old_path, new_path)

            session["username_updated"] = "Usuario actualizado"

            # Eliminar la clave 'user_username' de la sesión
            session.pop('user_username', None)
            # Crear la clave 'user_username' en la sesión con el nuevo valor
            session['user_username'] = update_new_user

            return redirect('/profile')
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})

# actualiza informacion del usuario
def update_p_data():
    idu = session.get('user_id')
    # busca el usuario correspondiente a la sesion
    update_user = user.query.get(idu)

    # toma los valores del formulario
    data = request.json

    # si no se ha enviado una contraseña se reemplaza por ''
    password = data.get('password', '')
    # se envio una contraseña
    if password != '':
        # toma la sal del usuario y la contraseña introducida
        salt = update_user.salt
        encoded_password = data['password']
        try:
            # cifra la constraseña nueva
            salted_password = str(salt) + encoded_password
            hash_object = hashlib.sha256(salted_password.encode('latin-1'))
            hashed_salted_password = hash_object.hexdigest()

            # envia correo avisando del cambio
            email = update_user.email
            name = data['firstname'] + " " + data['surname']
            password_changed_mail(email, name)

            # actualiza la información del usuario
            update_query = update(user).where(user.iduser == idu).values(
                name=data['firstname'],
                surname=data['surname'],
                username=data['username'],
                password=hashed_salted_password
            )
            db.session.execute(update_user)
            db.session.commit()

            session["username_updated"] = "Usuario actualizado"

            # Eliminar la clave 'user_username' de la sesión
            session.pop('user_name', None)
            # Crear la clave 'user_username' en la sesión con el nuevo valor
            session['user_name'] = data['username']

            return jsonify({'message': 'Profile updated successfully'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})

    # no se envio una clave nueva
    elif password == '':
        try:
            # actualiza la informacion del usuario
            update_query = update(user).where(user.iduser == idu).values(
                name=data['firstname'],
                surname=data['surname'],
                username=data['username']
            )

            db.session.execute(update_query)
            db.session.commit()

            session["username_updated"] = "Usuario actualizado"

            # Eliminar la clave 'user_username' de la sesión
            session.pop('user_name', None)
            # Crear la clave 'user_username' en la sesión con el nuevo valor
            session['user_name'] = data['username']

            return jsonify({'message': 'Profile updated successfully'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})

# verificacion antes de ejecutar el cambio de informacion del usuario
def auth_update():
    data = request.json

    # se verifica que los datos introducidos coincidan con los de la base de datos
    auth_email = session.get('user_email')
    ver_email = data['ver_email']
    ver_password = data['ver_password']

    get_auth_password = user.query.filter(user.email == ver_email).first()

    auth_password = get_auth_password.password
    salt = get_auth_password.salt

    try:
        salted_password = str(salt) + ver_password
        hash_object = hashlib.sha256(salted_password.encode('latin-1'))
        hashed_salted_password = hash_object.hexdigest()

        if auth_email == ver_email and hashed_salted_password == auth_password:
            return 'True'
        else:
            return 'False'
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error':str(e)})

def deactivate_account():
    data = request.json

    # se verifica que los datos introducidos coincidan con los de la base de datos
    auth_email = session.get('user_email')
    ver_email = data['ver_email']
    ver_password = data['ver_password']

    get_auth_password = user.query.filter(user.email == ver_email).first()

    auth_password = get_auth_password.password
    salt = get_auth_password.salt

    try:
        salted_password = str(salt) + ver_password
        hash_object = hashlib.sha256(salted_password.encode('latin-1'))
        hashed_salted_password = hash_object.hexdigest()

        # si coinciden
        if auth_email == ver_email and hashed_salted_password == auth_password:
            try:
                username = session.get('user_username')
                # rutas para limpiar los archivos del usuario desactivado
                _dir = f'c-cloud/userFiles/{username}/saved_files'
                recreate_old = f'c-cloud/userFiles/{username}/saved_files/old'
                recreate_trash = f'c-cloud/userFiles/{username}/saved_files/trash'

                path = os.path.join(_dir)
                path_old = os.path.join(recreate_old)
                path_trash = os.path.join(recreate_trash)

                # cambia el estado del usuario
                update_query = update(user).where(user.iduser == session.get('user_id')).values(
                    is_active = False
                )
                db.session.execute(update_query)
                db.session.commit()

                # envia correo de aviso
                email = auth_email
                name = get_auth_password.name + " " + get_auth_password.surname
                account_deactivated_user_mail(email, name)

                shutil.rmtree(path)
                os.makedirs(path_old)
                os.makedirs(path_trash)

                # limpia la sesion
                session.clear()
                return 'True'
            except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error':str(e)})
        else:
            return 'False'
    except Exception as e:
        print(traceback.formate_exc())
        return jsonify({'error':str(e)})

def control_deactivate_user():
    data = request.json
    iduser = data['user']
    try:
        user_info = user.query.filter(user.iduser == iduser).first()
        username = user_info.username
        email = user_info.email

        name = user_info.name + " " + user_info.surname
        account_deactivated_user_mail(email, name)

        # rutas para limpiar los archivos del usuario desactivado
        _dir = f'c-cloud/userFiles/{username}/saved_files'
        recreate_old = f'c-cloud/userFiles/{username}/saved_files/old'
        recreate_trash = f'c-cloud/userFiles/{username}/saved_files/trash'

        path = os.path.join(_dir)
        path_old = os.path.join(recreate_old)
        path_trash = os.path.join(recreate_trash)

        # cambia el estado del usuario
        update_query = update(user).where(user.iduser == iduser).values(
            is_active = False
        )
        db.session.execute(update_query)
        db.session.commit()

        shutil.rmtree(path)
        os.makedirs(path_old)
        os.makedirs(path_trash)

        return "User deactivated successfully"
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error':str(e)})

def control_reactivate_user():
    data = request.json
    iduser = data['user']
    try:
        # cambia el estado del usuario de inactivo a activo
        user_info = user.query.filter(user.iduser == iduser).first()
        email = user_info.email

        send_mail(email, 'Su cuenta ha sido reactivada', '')

        update_query = update(user).where(user.iduser == iduser).values(
            is_active = True
        )
        db.session.execute(update_query)
        db.session.commit()

        return "User reactivated successfully"
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error':str(e)})

def control_update_user():
    data = request.json
    iduser = int(data['user'])
    new_role = int(data['role'])

    # cambia el rol y estado del usuario
    if data['status'] == '1':
        new_status = True
    elif data['status'] == '0':
        new_status = False

    try:
        update_query = update(user).where(user.iduser == iduser).values(
            is_active = new_status,
            usertype = new_role
        )

        db.session.execute(update_query)
        db.session.commit()

        return "User updated successfully"
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error':str(e)})

def control_update_licence():
    data = request.json

    # actualiza la informacion de la licencias
    idlicence = int(data['licence'])
    new_price = float(data['price'])
    new_max_storage = int(data['max_storage'])
    new_file_capacity = int(data['file_capacity'])

    if data['support_24_7'] == '1':
        new_support_24_7 = True
    elif data['support_24_7'] == '0':
        new_support_24_7 = False

    if data['auto_backups'] == '1':
        new_auto_backups = True
    elif data['auto_backups'] == '0':
        new_auto_backups = False

    if data['secure_access'] == '1':
        new_secure_access = True
    elif data['secure_access'] == '0':
        new_secure_access = False


    try:
        update_query = update(licence).where(licence.idlicence == idlicence).values(
            price = new_price,
            max_storage_mb = new_max_storage,
            support_24_7 = new_support_24_7,
            automatic_backups = new_auto_backups,
            secure_access = new_secure_access,
            file_capacity = new_file_capacity
        )

        db.session.execute(update_query)
        db.session.commit()

        return "Licence updated successfully"
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error':str(e)})