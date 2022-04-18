# This module will be in charge of hashing and validating the passwords.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_hasher(pwd):
    hashed_password = pwd_context.encrypt(pwd)
    return hashed_password

def password_validator(hashed_pwd, pwd):
    if pwd_context.verify(hashed_pwd, pwd) == True:
        return True
    else:
        return False

