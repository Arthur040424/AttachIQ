import bcrypt

def hash_password(plain_password: str) -> str:
    """ Hash a plain password using bcrypt"""
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")