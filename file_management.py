from flask import request, session, send_file
from db_models import db, file, detailsfile
import os, traceback, builtins, datetime

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

def load_file__blank():
    username = session.get('user_username')
    filename = request.form['filename']
    directory = "userFiles/" + username + "/saved_files/"
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        try:
            return send_file(file_path, as_attachment=True)
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

def save_file(filename, extension, directory, filepath, content):
    with builtins.open(filepath, 'r') as r:
        old_content = r.read()
        
        old_version_date = os.path.getmtime(filepath) #2023-10-10 ...
        old_filename = f"{filename}_{old_version_date}{extension}" # title_2023-10-19(...).ext
        old_file = os.path.join(directory, old_filename)
        with builtins.open(old_file, 'w') as f:
            f.write(old_content)
            
            new_file = os.path.join(directory, filename + extension)
            
            with builtins.open(new_file, 'w') as n:
                n.write(content)
                return "File saved successfully"
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
    if os.path.exists(filepath):
        save_file(filename, extension, directory, filepath, content)
    elif not os.path.exists(filepath):
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
                except:
                    return traceback.print_exc()
            except:
                return traceback.print_exc()
        return 'File created successfully'

    
    
# filename = data['filename']
#     extension = data['extension']
#     content = data['content']
#     filepath = os.path.join(str(username_dir), filename + '.' + extension)
#     filepath = os.path.join(str(username_dir), toStandardName(filename) + '.' + extension)
#     with open(filepath, 'w') as f:
#         f.write(content)
#     return 'File created successfully'