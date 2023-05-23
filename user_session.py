from flask import render_template, request, redirect, session
import traceback

from db_models import db, user,  error, sessions
from hash import hash_password, check_credentials
from createUserFolder import newUserFolder, toStandardName
from sendMail import send_mail

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
            except:
                traceback.print_exc()
                return error
        else:
            return redirect('/login')
    else:
        return render_template('login.html', title=title)