from flask import request, session
import os

def create_file():
    username = session.get('user_iduser')
    data = request.json
    filename = data['filename']
    extension = data['extension']
    content = data['content']
    
    folder_path = "userFiles/" + username + "/saved_files/" + filename + "." + extension
    filepath = os.path.join(folder_path)
    with open(filepath, 'w') as f:
        f.write(content)
    return 'File created successfully'
