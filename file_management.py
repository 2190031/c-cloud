from flask import request, session
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
            return content, filename
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

def load_file__blank():
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
            return content, filename
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

def save_file():
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
            return content, filename
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'