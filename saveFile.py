from flask import request
import os

def create_file():
    data = request.json
    filename = data['filename']
    extension = data['extension']
    content = data['content']
    filepath = os.path.join(os.getcwd(), 'saved_files', filename + '.' + extension)
    with open(filepath, 'w') as f:
        f.write(content)
    return 'File created successfully'
