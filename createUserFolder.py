import os

def toStandardName(string):
    susername = string.split()
    return "_".join(susername)

def toNonStandardName(string):
    nusername = string.split("_")
    return " ".join(nusername)

def newUserFolder(username):
    s_username = toStandardName(username)
    dir = f"userFiles/{s_username}/saved_files"
    account_settings_dir = f"userFiles/{s_username}/acc_settings"
    acc_profile_pic = f"userFiles/{s_username}/acc_settings/profile_pic"

    # Ruta completa de la carpeta hija
    path_a = os.path.join(dir)
    path_b = os.path.join(account_settings_dir)
    path_c = os.path.join(acc_profile_pic)

    # Crear la carpeta hija si no existe
    if not os.path.exists(path_a):
        try:
            os.makedirs(path_a)
            os.makedirs(path_b)
            os.makedirs(path_c)
            print("Folder creado correctamente.")
        except OSError:
            print(f"Error al crear el folder {s_username}.")
    else:
        print("La carpeta ya existe")