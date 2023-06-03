from flask import render_template, request, redirect, session, jsonify
import traceback, hashlib, logging
from sqlalchemy import update

from google_auth_oauthlib.flow import Flow
from db_models import db, user,  error, sessions
from hash import hash_password, check_credentials
from createUserFolder import newUserFolder, toStandardName
from sendMail import send_mail

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
                subject = 'Bienvenido a C-Cloud'
                message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut pellentesque, nibh quis gravida mattis, diam neque rhoncus dui, eget bibendum mauris eros non dolor. Etiam ullamcorper mi at nisl placerat viverra. Integer ligula sapien, malesuada vel hendrerit vel, efficitur at neque. Maecenas ornare lobortis fermentum. Duis posuere urna odio, sed aliquet mauris laoreet at. Praesent lobortis congue scelerisque. Mauris non viverra ex. Vestibulum ullamcorper nisl ac leo lobortis, sed rutrum urna cursus. Etiam non nibh dolor. Praesent quis leo at turpis posuere molestie. Pellentesque enim leo, laoreet quis tincidunt non, pulvinar a ligula. Duis vitae lacus urna. Morbi ac consequat sapien. Nullam luctus nec massa hendrerit rhoncus. Phasellus id ipsum non mi laoreet blandit at id eros. Duis tortor lorem, ultricies nec sagittis vitae, porttitor at enim.'

                send_mail(email, subject, message)
                traceback.print_exc()
                return redirect('/login')
            except:
                traceback.print_exc()
                return error
        else:
          return render_template('sign_up.html', title=title)
        
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
                return redirect('/login')
        else:
            return render_template('login.html', title=title)
    
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

            # update_user.name = data['firstname']
            # update_user.surname  = data['surname']
            # update_user.username  = data['username']
            # update_user.password  = hashed_salted_password

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
            # update_user.firstname = data['firstname']
            # update_user.surname  = data['surname']
            # update_user.username  = data['username']

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
        return jsonify({'error': str(e)})