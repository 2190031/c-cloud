import os, traceback, builtins, datetime, base64

from flask import request, session, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from db_models import db, file, detailsfile, change, historial, user, error, preference

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
            return content
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

def load_file__blank(file):
    print(file)
    username = session.get('user_username')
    filename =  file # request.form['filename']
    directory = "userFiles/" + username + "/saved_files/"
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        try:
            return redirect(url_for("editor", o_filename=file))
            # return redirect(url_for("editor", o_content=content))
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

def save_file(filename, extension, directory, filepath, content):
    old_files_folder = 'old/'
    old_files_directory = os.path.join(directory + old_files_folder)
    with builtins.open(filepath, 'r') as r:
        old_content = r.read()
        
        old_version_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)) #2023-10-10 ...
        old_filename = f"{filename}_{old_version_date.strftime('%Y-%m-%d_%H_%M_%S')}{extension}" # title_2023-10-19(...).ext
        old_file = os.path.join(old_files_directory, old_filename)
        with builtins.open(old_file, 'w') as f:
            f.write(old_content)
            
            new_file = os.path.join(directory, filename + extension)
            
            with builtins.open(new_file, 'w') as n:
                n.write(content)
                try:
                    # idfile = db.session.query(file, user, detailsfile).join(file, detailsfile.idfile == file.idfile).join(user, detailsfile.iduser == session.get('user_id')).filter_by().first()
                    query = db.session.query(file.idfile).\
                    join(detailsfile, detailsfile.idfile == file.idfile).\
                    join(user, user.iduser == detailsfile.iduser).\
                    filter(user.iduser == session.get('user_id'))
                    
                    u_file = query.first()
                    
                    date = datetime.datetime.now()
                    now = date.strftime("%Y-%m-%d %H:%M:%S")
                    print(now, u_file)
                    historial_change = historial(
                        idfile       = u_file.idfile,
                        datemodified = now,
                        iduser       = session.get('user_id')
                    )
                    db.session.add(historial_change)
                    db.session.commit()
                    try:
                        idchange = historial.query.filter_by(
                            datemodified=now, iduser=session.get('user_id'), idfile=u_file.idfile
                        ).first()
                        
                        new_change =  change(
                            idchange     = idchange.idchange,
                            beforechange = old_content,
                            afterchange  = content
                        )
                        db.session.add(new_change)
                        db.session.commit()
                        return "File saved successfully"
                    except Exception as e:
                        print(traceback.format_exc())
                        return jsonify({'error': str(e)})
                except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})
                
            # almacenar el cambio en su tabla (revisar)

def create_file():
    username = session.get('user_username') 
    data = request.json
    filename = data['filename']
    extension = '.' + data['extension']
    content = data['content']
    directory = "userFiles/" + username + "/saved_files/"
    filepath = os.path.join(directory, filename + extension)
    print(filepath)
    new_file = file(
        name      = filename + extension,
        category  = 'something',
        extension = extension,
    )
    if os.path.exists(filepath): # If the file already exists, update and create a backup copy
        try:
            save_file(filename, extension, directory, filepath, content)
            return 'File saved successfully'
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})  # Return an error response as JSON
    elif not os.path.exists(filepath): # If the file doesn't exist, create a new file
        with builtins.open(filepath, 'w') as f:
            f.write(content)
            try:
                db.session.add(new_file)
                db.session.commit()
                id = new_file.idfile
                try:
                    detail = detailsfile(
                        idfile      = id,
                        iduser      = session.get('user_id'),
                        datecreated = datetime.datetime.now()
                    )
                    db.session.add(detail)
                    db.session.commit()
                    return 'File created successfully'
                except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})  # Return an error response as JSON
            except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})

def send_error_report():
    data = request.json
    iduser = session.get('user_id')
    report = data['report']
    date = datetime.datetime.now()
    
    new_report = error(
        iduser=iduser,
        description=report,
        datereported=date
    )
    
    try:
        db.session.add(new_report)
        db.session.commit()
        return "Report submited successfully"   
    except:
        return traceback.print_exc()
    
def save_preference():
    iduser = session.get('user_id')
    data = request.json
    font = data['font']
    size = data['size']
    theme = data['theme']
    
    new_pref = preference(
        iduser     = iduser,
        font       = font,
        fontsize   = size,
        theme      = theme
    )
    
    try:
        db.session.add(new_pref)
        db.session.commit()
        return "Preference submited successfully"   
    except:
        return traceback.print_exc()

def upload_p_picture():
    username = session.get('user_username')
    data = request.json
    
    image_b64 = data['image']
    
    _dir = f'userFiles/{username}/acc_settings/profile_pic'
    
    # check if the file has been uploaded
    if image_b64:
        # strip the leading path from the file name
        
        image_data = image_b64.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        fn = secure_filename('profile_pic.png') #os.path.basename(fileitem)
        
        path = os.path.join(_dir, fn)
       # open read and write the file into the server
        try:
            with open(path, 'wb') as f:
                f.write(image_bytes)
            return jsonify({'message': 'Profile picture uploaded successfully'})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'No image file received'})