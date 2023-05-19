import os

def newUserFolder(username):
    files_dir = "/saved_files"
    dir = f"userFiles/{username}/saved_files"

    # Ruta completa de la carpeta hija
    path = os.path.join(dir)

    # Crear la carpeta hija si no existe
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print("Folder creado correctamente.")
        except OSError:
            print(f"Error al crear el folder {username}.")
    else:
        print("La carpeta ya existe")