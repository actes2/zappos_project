import bcrypt


def encrypt_password(password, pepper=b"duck"):
    salted_pwd = password.encode("utf-8") + pepper
    return bcrypt.hashpw(salted_pwd, bcrypt.gensalt())


def check_password(password):
    enc_pass = encrypt_password(password)

    bcrypt.checkpw()
    if password == enc_pass:
        return True
    return False
