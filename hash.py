import hashlib, os, traceback
from db_models import user

def hash_password(password):
    try:
        # se genera una cadena de caracteres aleatorios con un valor menor a 127 en el codigo ascii
        salt = str(bytes([i for i in os.urandom(16) if i <= 127]))

        encoded_password = password

        # separa el identificador de bytes de salt b'...' y toma solo la cadena, lo concatena a la encoded_password
        salted_password = salt.split("'")[1] + encoded_password

        # usa hash en salted_password con SHA-256, codificado en latin-1
        hash_object = hashlib.sha256(salted_password.encode('latin-1'))

        # compara la contraseña traida de la base de datos con la cifrada
        hashed_password = hash_object.hexdigest()

        return (hashed_password, salt.split("'")[1])
    except Exception:
        print(traceback.format_exc())
        return None, None

def check_credentials(email, password):
    # retrieve the user with the given email
    User = user.query.filter_by(email=email).first()
    if User is None:
        # El usuario no existe
        return False

    # Toma la sal y contraseñas del usuario
    salt = User.salt
    hashed_password = User.password

    encoded_password = password

    # Añade la sal tomada de la consulta a la contraseña sin cifrado
    salted_password = salt + encoded_password

    # usa hash en salted_password con SHA-256, codificado en latin-1
    hash_object = hashlib.sha256(salted_password.encode('latin-1'))

    # convierte hash_object a caracteres hexagesimales
    hashed_salted_password = hash_object.hexdigest()

    # compara la contraseña traida de la base de datos con la cifrada
    if hashed_salted_password == hashed_password:
        return True
    else:
        return False