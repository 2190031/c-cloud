import hashlib, os

from db_models import user

def hash_password(password):
    try:
        salt = str(bytes([i for i in os.urandom(16) if i <= 127]))

        encoded_password = password

        salted_password = salt.split("'")[1] + encoded_password
        
        hash_object = hashlib.sha256(salted_password.encode('latin-1'))
        hashed_password = hash_object.hexdigest()
        return (hashed_password, salt.split("'")[1])
    except:
        print('error')

def check_credentials(email, password):
    # retrieve the user with the given email
    User = user.query.filter_by(email=email).first()
    if User is None:
        # user with the given email does not exist
        return False
    
    # decode the stored salt and hashed password from bytes to strings
    salt = User.salt
    hashed_password = User.password
    
    # concatenate the salt and password provided by the user
    encoded_password = password
    salted_password = str(salt) + encoded_password
    
    # hash the salted password using SHA-256
    hash_object = hashlib.sha256(salted_password.encode('latin-1'))

    hashed_salted_password = hash_object.hexdigest()
    
    # compare the hashed salted password to the stored hashed password
    if hashed_salted_password == hashed_password:
        # password is correct
        return True
    else:
        # password is incorrect
        return False