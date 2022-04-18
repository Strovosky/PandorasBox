# Here we'll create the new pandorausers or new misteries.

from fastapi import APIRouter, Depends, status, Body, Form, HTTPException
from config.db_config import local_session
from models.pydantic_models import MisteryBase, PandorasUsers, PandorasUsersOut
from schemas.db_models import PandorasUsersDB, PandorasMisteriesDB
from security.jwt_handler import ALGORITHM, SECRET_KEY
from security.password_encript import password_hasher
from security.authentication_paths import oauth2_scheme, user_id_getter
from jose import jwt, exceptions


app_create = APIRouter()


@app_create.post(
    path="/singup",
    summary="On this endpoint you can sing up to Pandora's Box.",
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    response_model=PandorasUsersOut)
def create_new_user(user: PandorasUsers = Body(...)):
    """
    ***Create New User***

    This endpoint will let you signup in Pandora's Box.

    Parameters:
    - ***user***: PandorasUsers, it's a Body type.

    Returns a confirmation message that the user was created.
    """
    all_users = local_session.query(PandorasUsersDB).all()

    if user.username in all_users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Error": "Username already exists"})

    for db_user in all_users:
        if user.first_name == db_user.first_name and user.last_name == db_user.last_name:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Error": "User already exists. You should reactivate the account."})


    db_user = PandorasUsersDB(
        first_name=user.first_name.title(),
        last_name=user.last_name.title(),
        username=user.username.title(),
        hashed_password=password_hasher(user.password)
    )
    if user.email:
        db_user.email = user.email
    if user.cellphone:
        db_user.cellphone = user.cellphone
    
    local_session.add(db_user)
    local_session.commit()

    return user

@app_create.put(
    path="/reactivate-account",
    summary="Here you will be able to reactivate an old account you had.",
    tags=["Users"])
def reactivate_account(
    first_name: str = Form(..., max_length=60),
    last_name: str = Form(..., max_length=70)):
    all_disabled_users = local_session.query(PandorasUsersDB).filter(PandorasUsersDB.disabled == True).all()

    if not all_disabled_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "There are no disabled accounts at the moment"})

    for disabled_user in all_disabled_users:
        if disabled_user.first_name == first_name.title() and disabled_user.last_name == last_name.title():
            disabled_user.disabled = False
            return {"Status": f"Your account {disabled_user.username} has been recovered"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "Disabled Account Not Found"})


# On this endpoint I need to pass the token, so I can get who the user is and pass their foreign_key.
@app_create.post(
    path="/new-mistery",
    summary="This endpoint let's you create a new mistery.",
    status_code=status.HTTP_201_CREATED,
    tags=["Misteries"],
    response_model=MisteryBase)
def new_mistery(new_mistery: MisteryBase = Body(...), token: str =  Depends(oauth2_scheme)):
    """
    ***Create New Mistery***

    This endpoint will let you create a new Pandora's Box's mistery.

    Parameters:
    - ***new_mistery***: MisteryBase, it's a Body type.
    - ***token***: Depends.

    Returns the info of the mistery created.
    """

    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Signature.")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Valid Token.")

    user_id = user_id_getter(token)

    db_mistery = PandorasMisteriesDB(
        mistery_title=new_mistery.mistery_title.title(),
        password=new_mistery.password,
        foreign_key=user_id,
        username=new_mistery.username
    )

    if new_mistery.mistery_token:
        db_mistery.mistery_token = new_mistery.mistery_token
    if new_mistery.email:
        db_mistery.email = new_mistery.email
    if new_mistery.description:
        db_mistery.description = new_mistery.description
    if new_mistery.url:
        db_mistery.url = new_mistery.url
    if new_mistery.other:
        db_mistery.other = new_mistery.other
    
    local_session.add(db_mistery)
    local_session.commit()

    return new_mistery
