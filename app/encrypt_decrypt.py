import bcrypt


def encrypt_password(password, pepper="duck"):
    peppered_pwd = (password + pepper).encode("utf-8")
    return bcrypt.hashpw(peppered_pwd, bcrypt.gensalt())


def check_password(password, hash_passwd, pepper="duck"):

    peppered_pwd = (password + pepper).encode("utf-8")

    result = bcrypt.checkpw(peppered_pwd, hash_passwd.encode('utf-8'))

    if result:
        return True
    return False
