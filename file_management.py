from flask import request, session, send_file
import os
import builtins

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

def save_file():
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

    
    
# filename = data['filename']
#     extension = data['extension']
#     content = data['content']
#     filepath = os.path.join(str(username_dir), filename + '.' + extension)
#     filepath = os.path.join(str(username_dir), toStandardName(filename) + '.' + extension)
#     with open(filepath, 'w') as f:
#         f.write(content)
#     return 'File created successfully'