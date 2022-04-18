# In this module, we'll let our users log in.

from fastapi import APIRouter, status, Depends
from models.pydantic_models import PandorasUserLogin
from fastapi.security import OAuth2PasswordRequestForm # This one will request the username and password.
from fastapi.security import OAuth2PasswordBearer # To request authentication
from schemas.db_models import PandorasUsersDB
from config.db_config import local_session
from fastapi.responses import JSONResponse
from security.password_encript import password_validator
from security.jwt_handler import token_writer, validate_token
from jose import jwt
from security.jwt_handler import SECRET_KEY, ALGORITHM



app_authentication = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token_url")


@app_authentication.post(path="/token_url", summary="This endpoint will let the users get authenticated.", tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = local_session.query(PandorasUsersDB).filter(PandorasUsersDB.username == form_data.username).first()
    
    user_login = PandorasUserLogin(username=form_data.username, password=form_data.password)
    
    if not user:
        return JSONResponse(content={"Error": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)

    if password_validator(user_login.password, user.hashed_password) == False:
        return JSONResponse(content={"Error": "Wrong Password"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    if user.disabled:
        return JSONResponse(content={"Error": "User's account is disabled"}, status_code=status.HTTP_401_UNAUTHORIZED)

    token = token_writer({"sub": str(user.user_id)})

    return {"access_token": token, "token_type": "bearer"}


def user_id_getter(token):
    payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    return user_id
