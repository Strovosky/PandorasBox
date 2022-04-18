# This module will manage the creation, validation, and returning of jwt tokens.

from decouple import config # To manage the info in the .env file.

from datetime import datetime, timedelta # To create the expiration time for the jwt.
from jose import jwt, exceptions
from fastapi.responses import JSONResponse
from fastapi import status

SECRET_KEY = config("SECRET")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def expiration_date_creator(expiration_time):
    return datetime.utcnow() + timedelta(minutes=expiration_time)

def token_writer(data: dict):
    token = jwt.encode(
        claims={**data, "exp": expiration_date_creator(ACCESS_TOKEN_EXPIRE_MINUTES)},
        key=SECRET_KEY,
        algorithm=ALGORITHM)
    return token

def validate_token(token):
    try:
        jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Expired Token"}, status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=status.HTTP_401_UNAUTHORIZED)
