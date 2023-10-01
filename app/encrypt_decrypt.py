import bcrypt


def encrypt_password(password, pepper=b"duck"):
    salted_pwd = password.encode("utf-8") + pepper
    return bcrypt.hashpw(salted_pwd, bcrypt.gensalt())


def check_password(password, password_attempt):
    pass
