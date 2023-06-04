import traceback, hashlib, logging, secrets, os, pathlib, google, requests, cachecontrol

from flask import render_template, request, redirect, session, jsonify, abort

from sqlalchemy import update
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token

from db_models import db, user,  error, sessions
from hash import hash_password, check_credentials
from createUserFolder import newUserFolder, toStandardName
from sendMail import send_mail

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
    redirect_uri="http://127.0.0.1:5000/callback",
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
            newsession = sessions(iduser=id)
            try:
                db.session.add(newsession)
                db.session.commit()

                _iduser = user.query.filter_by(google_id = googleid).first()
                print(_iduser)

                session["user_id"] = _iduser.iduser
                session["user_name"] = google_name
                session["user_email"] = id_info.get("email")
                session["google_picture"] = id_info.get("picture")
                session["user_username"] = google_user_verify.username

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
            session["success"] = "Inicie sesión nuevamente"
            return redirect("/login")
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



def signup():
    title = 'Registrarse'
    if "google_id" in session or "user_id" in session:
       return redirect("/")
    else:
        if request.method == 'POST':
            name     = request.form.get('name')
            surname  = request.form.get('surname')
            username = request.form.get('username')
            email    = request.form.get('email')
            password = request.form.get('password')
            usertype = request.form.get('usertype', 1)
            path = f'userFiles/{username}/acc_settings/profile_pic/profile_pic.png'
            verify_email = user.query.filter_by(email=email).first()
            if verify_email:
                session["error"] = "El correo que proporcionaste está registrado. Debe iniciar sesión si quiere acceder conél."
                return redirect("/signup")
            else:
                hashed_password, salt = hash_password(password)
                newuser = user( name        =name, 
                                surname     =surname, 
                                username    =username, 
                                email       =email, 
                                password    =hashed_password,
                                salt        =salt, 
                                picture     =path, 
                                usertype    =usertype)
                try:
                    print(hashed_password)
                    db.session.add(newuser)
                    db.session.commit()
                    newUserFolder(username)
                    subject = 'Bienvenido a C-Cloud'
                    message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut pellentesque, nibh quis gravidamattis, diam neque rhoncus dui, eget bibendum mauris eros non dolor. Etiam ullamcorper mi at nislplacerat viverra. Integer ligula sapien, malesuada vel hendrerit vel, efficitur at neque. Maecenasornare lobortis fermentum. Duis posuere urna odio, sed aliquet mauris laoreet at. Praesent lobortiscongue scelerisque. Mauris non viverra ex. Vestibulum ullamcorper nisl ac leo lobortis, sed rutrum urnacursus. Etiam non nibh dolor. Praesent quis leo at turpis posuere molestie. Pellentesque enim leo,laoreet quis tincidunt non, pulvinar a ligula. Duis vitae lacus urna. Morbi ac consequat sapien. Nullamluctus nec massa hendrerit rhoncus. Phasellus id ipsum non mi laoreet blandit at id eros. Duis tortorlorem, ultricies nec sagittis vitae, porttitor at enim.'
                    send_mail(email, subject, message)
                    session["success"] = "Inicie sesión nuevamente"
                    return redirect('/login')
                except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})
        else:
            success_message = session.pop("success", None)
            error_message = session.pop("error", None)
            return render_template('sign_up.html', title=title, success_message=success_message, error_message=error_message)
        
def login():
    if "google_id" in session or "user_id" in session:
        return redirect('/')
    else:
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
                except:
                    traceback.print_exc()
                    return error
            else:
                session["error"] = "Credenciales incorrectas."
                return redirect('/login')
        else:
            success_message = session.pop("success", None)
            error_message = session.pop("error", None)
            return render_template('login.html', title=title, error_message=error_message, success_message=success_message)
    
def update_p_data():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    idu = session.get('user_id')
    update_user = user.query.get(idu)
    data = request.json
    password = data.get('password', '')
    print(update_user)
    
    if password != '':
        salt = update_user.salt
        encoded_password = data['password']
        try:
            salted_password = str(salt) + encoded_password
            hash_object = hashlib.sha256(salted_password.encode('latin-1'))
            hashed_salted_password = hash_object.hexdigest()

            email = update_user.email
            subject = 'Cambio de contraseña'
            message = f'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut pellentesque, nibh quis gravida mattis, diam neque rhoncus dui, eget bibendum mauris eros non dolor. Etiam ullamcorper mi at nisl placerat viverra. Integer ligula sapien, malesuada vel hendrerit vel, efficitur at neque. Maecenas ornare lobortis fermentum. Duis posuere urna odio, sed aliquet mauris laoreet at. Praesent lobortis congue scelerisque. Mauris non viverra ex. Vestibulum ullamcorper nisl ac leo lobortis, sed rutrum urna cursus. Etiam non nibh dolor. Praesent quis leo at turpis posuere molestie. Pellentesque enim leo, laoreet quis tincidunt non, pulvinar a ligula. Duis vitae lacus urna. Morbi ac consequat sapien. Nullam luctus nec massa hendrerit rhoncus. Phasellus id ipsum non mi laoreet blandit at id eros. Duis tortor lorem, ultricies nec sagittis vitae, porttitor at enim.\
            \nSu nueva contraseña es {encoded_password}'
            send_mail(email, subject, message)
            
            print(update_user)
            
            update_query = update(user).where(user.iduser == idu).values(
                name=data['firstname'],
                surname=data['surname'],
                username=data['username'],
                password=hashed_salted_password
            )
            db.session.execute(update_user)
            db.session.commit()
            
            return jsonify({'message': 'Profile updated successfully'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})
    elif password == '':
        try:
            update_query = update(user).where(user.iduser == idu).values(
                name=data['firstname'],
                surname=data['surname'],
                username=data['username']
            )

            print(update_query)
            db.session.execute(update_query)
            db.session.commit()
            
            return jsonify({'message': 'Profile updated successfully'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})

def auth_update():
    data = request.json
    
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
        
        print(f'Input: {hashed_salted_password} \n\nExpected: {auth_password}')
        
        if auth_email == ver_email and hashed_salted_password == auth_password:
            return 'True'
        else:
            return 'False'
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error':str(e)})