import os
import traceback
import builtins
import datetime
import base64
import io
import mimetypes
import asyncio
import aiofiles
import sys
import logging

sys.path.append('c-cloud/venv')

from flask import request, session, jsonify, redirect, url_for
from sqlalchemy import update, desc
from werkzeug.utils import secure_filename
from db_models import db, licence, paytransaction, user, error, file, detailsfile, change, historial, preference
from PIL import Image

def load_file():
    username = session.get('user_username')
    filename = request.form['filename']
    directory =  "c-cloud/userFiles/" + username + "/saved_files/"
    file_path = os.path.join(directory, filename)

    print(file_path)

    if os.path.isfile(file_path):
        try:
            with builtins.open(file_path, 'r') as f:
                lines = f.read()
            content = lines #'\n'.join(line for line in lines if not line.isspace())
            return content
        except FileNotFoundError:
            return "No file found"
    else:
        return 'File not found'

def load_file__blank(file):
    print(file)
    username = session.get('user_username')
    filename =  file # request.form['filename']
    directory = "c-cloud/userFiles/" + username + "/saved_files/"
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
    content_bytes = content.encode('utf-8')
    size_in_bytes = len(content_bytes)

    print("-------")
    print(size_in_bytes)
    print("-------")
    if check_max_storage_with_new(directory, size_in_bytes):
         with builtins.open(filepath, 'r') as r:
            old_content = r.read()

            old_version_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            old_filename = f"{filename}_{old_version_date.strftime('%Y-%m-%d_%H_%M_%S')}{extension}"
            old_file = os.path.join(old_files_directory, old_filename)
            with builtins.open(old_file, 'w') as f:
                f.write(old_content)

                new_file = os.path.join(directory, filename + extension)

                with builtins.open(new_file, 'w') as n:
                    n.write(content)
                    try:
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
                            return "Archivo guardado exitosamente."
                        except Exception as e:
                            print(traceback.format_exc())
                            return jsonify({'error': str(e)})
                    except Exception as e:
                        print(traceback.format_exc())
                        return jsonify({'error': str(e)})
    else:
        return "No se puede guardar el archivo. El espacio de almacenamiento máximo se ha alcanzado."

    return "Archivo guardado exitosamente."


def check_max_storage(directory):
    total_size = 0
    session_user_storage = actual_licence(session.get("user_id"))

    for dirpath, _, filenames in os.walk(directory):
        # Excluir la carpeta "old"
        if 'old' in dirpath:
            continue
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    total_size_mb = total_size / (1024 * 1024)  # Convertir bytes a megabytes
    total_size_mb_rounded = round(total_size_mb, 2)  # Redondear a 2 decimales

    if total_size_mb_rounded > session_user_storage:
        return True
    else:
        return False

def check_max_storage_with_new(directory, content):
    total_size = 0
    session_user_storage = actual_licence(session.get("user_id"))

    for dirpath, _, filenames in os.walk(directory):
        # Excluir la carpeta "old"
        if 'old' in dirpath:
            continue
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    total_size_bytes = content+total_size
    total_size_mb = total_size_bytes / 1048576 # Convertir bytes a megabytes
    total_size_mb_rounded = round(total_size_mb, 2)  # Redondear a 2 decimales
    print(content)
    print(total_size_bytes)
    print(total_size_mb)
    print(total_size_mb_rounded)
    print(session_user_storage)
    if session_user_storage > total_size_mb_rounded:
        return True
    else:
        return False

def calculate_total_space(directory):
    total_size = 0

    for dirpath, _, filenames in os.walk(directory):
        # Excluir la carpeta "old"
        if 'old' in dirpath:
            continue
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    total_size_kb = total_size / 1024  # Convertir bytes a kilobytes

    if total_size_kb > 1024:
        total_size_mb = total_size_kb / 1024  # Convertir kilobytes a megabytes
        return total_size_mb, ' MB'
    else:
        return total_size_kb, ' KB'

def actual_licence(id_user):
        last_transaction = paytransaction.query.filter_by(iduser=id_user).order_by(desc(paytransaction.idpaytransaction)).first()
        if last_transaction:
            id_plan = licence.query.get(last_transaction.idlicence).idlicence
            id_licence = licence.query.filter_by(idlicence=id_plan).first()
            max_storage_mb = id_licence.max_storage_mb
            #print(max_storage_mb)
            return max_storage_mb
        else:
            id_plan = licence.query.get(3).idlicence
            id_licence = licence.query.filter_by(idlicence=id_plan).first()
            max_storage_mb = id_licence.max_storage_mb
            #print(max_storage_mb)
            return max_storage_mb

# Si mb = kb/1024 entonces kb = mb * 1024

def storage_per_archive(id_user):
        last_transaction = paytransaction.query.filter_by(iduser=id_user).order_by(desc(paytransaction.idpaytransaction)).first()
        if last_transaction:
            id_plan = licence.query.get(last_transaction.idlicence).idlicence
            id_licence = licence.query.filter_by(idlicence=id_plan).first()
            storage_per_capacity = id_licence.file_capacity

            return storage_per_capacity
        else:
            id_plan = licence.query.get(3).idlicence
            id_licence = licence.query.filter_by(idlicence=id_plan).first()
            storage_per_capacity = id_licence.file_capacity

            return storage_per_capacity

def create_file():
    username = session.get('user_username')
    data = request.json
    filename = data['filename']
    extension = '.' + data['extension']
    content = data['content']
    directory = f"c-cloud/userFiles/{username}/saved_files/"
    filepath = os.path.join(directory, filename + extension)
    print(filepath)
    max_storage_per_archive = storage_per_archive(session.get("user_id"))
    # Calcular el peso estimado del archivo en bytes
    content_size = len(content.encode('utf-8'))

    content_size_mb = content_size / 1048576
    # Obtener el tipo MIME del archivo
    mimetype, _ = mimetypes.guess_type(filepath)
    category = mimetype if mimetype else 'unknown'

    new_file = file(
        name=filename + extension,
        category=category,  # mime type
        extension=extension,
    )
    print(content_size)
    print(content_size_mb)
    if not check_max_storage_with_new(directory, content_size):
        return 'Has superado el espacio máximo'
    elif content_size_mb < max_storage_per_archive:
        if os.path.exists(filepath):  # If the file already exists, update and create a backup copy
            try:
                save_file(filename, extension, directory, filepath, content)
                return 'File saved successfully'
            except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})  # Return an error response as JSON
        elif not os.path.exists(filepath):  # If the file doesn't exist, create a new file
            with builtins.open(filepath, 'w') as f:
                f.write(content)
                try:
                    db.session.add(new_file)
                    db.session.commit()
                    id = new_file.idfile
                    try:
                        detail = detailsfile(
                            idfile=id,
                            iduser=session.get('user_id'),
                            datecreated=datetime.datetime.now()
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
    else:
        return 'El archivo excede el tamaño máximo permitido'


def delete_file(filename, extension):
    username = session.get('user_username')
    filepath = f'c-cloud/userFiles/{username}/saved_files/{filename}{extension}'
    trash_files_folder = f'c-cloud/userFiles/{username}/saved_files/trash/'
    trash_files_directory = os.path.join(trash_files_folder)
    with builtins.open(filepath, 'r') as r:
        to_delete_file_content = r.read()
        to_delete_file_version_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)) #2023-10-10 ...
        to_delete_file_filename = f"{filename}_{to_delete_file_version_date.strftime('%Y-%m-%d_%H_%M_%S')}{extension}" # title_2023-10-19(...).ext
        to_delete_file = os.path.join(trash_files_directory, to_delete_file_filename)
        with builtins.open(to_delete_file, 'w') as f: # Copia del archivo
            f.write(to_delete_file_content)

            # new_trash_file = os.path.join(directory, filename + extension)

            # with builtins.open(new_trash_file, 'w') as t: #Modificacion del archivo, cambiar aqui
            #     t.write(content)
            os.remove(filepath) #Eliminar el archivo de saved_files

            try: #Archivo ya copiado, se hacen consultas
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
                        beforechange = to_delete_file_content,
                        afterchange  = None
                    )
                    db.session.add(new_change)
                    db.session.commit()
                    return "File deleted successfully"
                except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})
            except Exception as e:
                    print(traceback.format_exc())
                    return jsonify({'error': str(e)})

def permanently_delete():
    data = request.json
    file = data['filename']
    username = session.get('user_username')
    _dir = f"c-cloud/userFiles/{username}/saved_files/trash"
    path = os.path.join(_dir, file)
    try:
        if os.path.exists(path):
            os.remove(path)
            return 'File deleted successfully'
        else:
            return jsonify({'error': str('File not found')})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)})

async def restore_file_async():
    username = session.get('user_username')
    data = request.json
    filename = data['filename']

    filepath = f'c-cloud/userFiles/{username}/saved_files/trash/'
    trash_folder_file = os.path.join(filepath, filename)

    saved_files_folder = f'c-cloud/userFiles/{username}/saved_files/'
    saved_files_directory = os.path.join(saved_files_folder, filename)
    async with aiofiles.open(trash_folder_file, 'r') as r:
        to_delete_file_content = await r.read()

        async with aiofiles.open(saved_files_directory, 'w') as f: # Copia del archivo
            await f.write(to_delete_file_content)

        try: #Archivo ya copiado, se hacen consultas
            # idfile = db.session.query(file, user, detailsfile).join(file, detailsfile.idfile == file.idfile).join(user, detailsfile.iduser == session.get('user_id')).filter_by().first()
            query = db.session.query(file.idfile).join(detailsfile, detailsfile.idfile == file.idfile).join(user, user.iduser == detailsfile.iduser).filter(user.iduser == session.get('user_id')).first()

            u_file = query

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

                new_change = change(
                        idchange     = idchange.idchange,
                        beforechange = to_delete_file_content,
                        afterchange  = None
                    )
                db.session.add(new_change)
                db.session.commit()

                await asyncio.sleep(1)

                return "File restored successfully"
            except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})
        except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})

def restore_file():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(restore_file_async())
    loop.close()
    username = session.get('user_username')
    filepath = f"c-cloud/userFiles/{username}/saved_files/trash/"
    data = request.json
    filename = data['filename']
    os.remove(os.path.join(filepath, filename)) #Eliminar el archivo de trash

def send_error_report():
    data = request.json
    iduser = session.get('user_id')
    topic = data['topic']
    report = data['report']
    date = datetime.datetime.now()

    new_report = error(
        iduser = iduser,
        topic = topic,
        description = report,
        datereported = date,
        is_resolved = False
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

    _dir = f'c-cloud/userFiles/{username}/acc_settings/profile_pic'

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

def get_profile_pic():
    usern = user.query.filter_by(iduser=session.get('user_id')).first()
    _dir = usern.picture
    path = os.path.join(_dir)

    if os.path.exists(path):
        with Image.open(path) as image:
        # Recortar la imagen en un cuadrado
            width, height = image.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = (width + size) // 2
            bottom = (height + size) // 2
            cropped_image = image.crop((left, top, right, bottom))

            # Convertir la imagen recortada a base64
            buffered = io.BytesIO()
            cropped_image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # # Retornar la imagen como respuesta en formato JSON
        return {'image': image_base64}
    else:
        return {'error': 'El archivo de imagen no existe'}

def download_file():
    username = session.get('user_username')
    data = request.json

    filename = data['filename']

    _dir = f"c-cloud/userFiles/{username}/saved_files"
    path = os.path.join(_dir, filename)

    try:
        with builtins.open(path, 'r') as r:
            content = r.read()
            return content
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)})


async def move_to_trash_async():
    username = session.get('user_username')
    data = request.json
    filename = data["filename"]

    filepath = f'c-cloud/userFiles/{username}/saved_files/'
    trash_filepath = f'c-cloud/userFiles/{username}/saved_files/trash/'

    _dir = os.path.join(filepath, filename)
    trash_dir = os.path.join(trash_filepath, filename)

    async with aiofiles.open(_dir, 'r') as r:
        to_delete_file_content = await r.read()

        async with aiofiles.open(trash_dir, 'w') as f: # Copia del archivo
            await f.write(to_delete_file_content)

        try: #Archivo ya copiado, se hacen consultas
            # idfile = db.session.query(file, user, detailsfile).join(file, detailsfile.idfile == file.idfile).join(user, detailsfile.iduser == session.get('user_id')).filter_by().first()
            query = db.session.query(file.idfile).join(detailsfile, detailsfile.idfile == file.idfile).join(user, user.iduser == detailsfile.iduser).filter(user.iduser == session.get('user_id')).first()

            u_file = query

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

                new_change = change(
                        idchange     = idchange.idchange,
                        beforechange = to_delete_file_content,
                        afterchange  = None
                    )
                db.session.add(new_change)
                db.session.commit()

                await asyncio.sleep(1)

                return "File restored successfully"
            except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})
        except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})

def move_to_trash():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(move_to_trash_async())
    loop.close()
    username = session.get('user_username')
    filepath = f"c-cloud/userFiles/{username}/saved_files/"
    data = request.json
    filename = data['filename']
    os.remove(os.path.join(filepath, filename)) #Eliminar el archivo de saved_files

def get_file_size(filename):
    try:
        username = session.get('user_username')
        _dir = f'c-cloud/userFiles/{username}/saved_files/'
        file = os.path.join(_dir, filename)
        file_size_bytes = os.path.getsize(file)
        file_size_kb = file_size_bytes / 1024

        if file_size_kb >= 100:
            file_size_mb = file_size_kb / 1024
            return file_size_mb, ' MB'
        else:
            return file_size_kb, ' KB'
    except FileNotFoundError:
        print("El archivo no existe.")
        return None

def mark_as_resolved():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    data = request.json
    report = int(data['report'])

    try:
        update_query = update(error).where(error.iderror == report).values(is_resolved=True)
        with db.session.begin():
            db.session.execute(update_query)
        return "Marked as resolved"
    except Exception as e:
        db.session.rollback()
        print(traceback.format_exc())
        return jsonify({'error': str(e)})


def validate_extension(filename, allowed_extensions):
    # Obtener la extensión del archivo
    extension = filename.rsplit('.', 1)[-1].lower()

    # Validar si la extensión está en la lista de extensiones permitidas
    if extension in allowed_extensions:
        return True
    else:
        return False

def upload_file():
    username = session.get('user_username')
    directory = f"c-cloud/userFiles/{username}/saved_files/"


    if check_max_storage(directory):
        return 'Has superado el espacio máximo'
    else:
        # Obtener el archivo enviado en la solicitud
        file = request.files['file']
        file_size = len(file.read())
        allowed_extensions = ['txt', 'html', 'js', 'css', 'py', 'php', 'c', 'java', 'sql', 'json', 'xml', 'csv', 'yaml', 'md', 'rb', 'swift', 'ts', 'go', 'rs', 'dart']
        # Validar si se recibió un archivo
        if file:
            # Validar la extensión del archivo
            filename = secure_filename(file.filename)
            if validate_extension(filename, allowed_extensions):
                # Validar el tamaño del archivo
                max_file_size = storage_per_archive(session.get("user_id"))
                max_file_size_byte = max_file_size * 1048576
                if len(file.read()) > max_file_size_byte:
                    return 'El archivo excede el tamaño máximo permitido por tu cuota'
                elif check_max_storage_with_new(directory, file_size):
                    file.seek(0)  # Volver a colocar el puntero del archivo al principio
                    # Guardar el archivo en la ruta especificada
                    filepath = os.path.join(directory, filename)
                    try:
                        file.save(filepath)

                        # Realizar las operaciones adicionales que necesites con el archivo subido

                        return 'Archivo subido correctamente'
                    except Exception:
                        return 'Error al guardar el archivo'
                else:
                    return 'No se puede subir porque supera el espacio máximo de tu cuota'
            else:
                return 'Extensión de archivo no permitida'
        else:
            return 'No se recibió ningún archivo'
