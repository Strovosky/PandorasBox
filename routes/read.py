# This module will be in charge of creating the endpoints to get the information in the database.

from fastapi import APIRouter, Form, HTTPException, status, Depends
from config.db_config import local_session
from schemas.db_models import PandorasUsersDB, PandorasMisteriesDB
from models.pydantic_models import MisteryOut, PandorasUsersOut
from security.authentication_paths import oauth2_scheme, user_id_getter
from jose import jwt, exceptions
from security.jwt_handler import ALGORITHM, SECRET_KEY


app_read = APIRouter()


def get_active_misteries(misteries):
    all_my_active_misteries = set()
    for mistery in misteries:
        if not mistery.disabled:
            all_my_active_misteries.add(mistery)
    return all_my_active_misteries


# This path operation was depracated
# I might activated if I want to create an admin account.
@app_read.get(
    path="/all-users",
    summary="This endopion will show all users in database.",
    tags=["Users"],
    deprecated=True)
def read_all_users(token: str = Depends(oauth2_scheme)):
    """
    ***Read All Users***

    This endpoint let's us read all the users in the database.

    Parameters:
    - 

    Returns a dictionary containing all the users.
    """
    
    all_users = local_session.query(PandorasUsersDB).all()
    return {"All Users": all_users}


@app_read.get(
    path="/all-my-misteries",
    summary="This endpoint let's you read all the misteries.",
    tags=["Misteries"])
def read_all_misteries(token: str = Depends(oauth2_scheme)):
    """
    ***All My Misteries***

    This endpoint reads all the misteries in the database.

    Parameters:
    - ***token***: str.

    Returns a dictionary will all the misteries.
    """
    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    user_id = user_id_getter(token)

    all_my_misteries = local_session.query(PandorasMisteriesDB).filter(PandorasMisteriesDB.foreign_key == int(user_id)).all()
    
    my_misteries = {}

    for ind, my_mistery in enumerate(all_my_misteries, start=1):
        if not my_mistery.disabled:
            mistery = MisteryOut(
                mistery_id=my_mistery.mistery_id,
                mistery_title=my_mistery.mistery_title,
                password=my_mistery.password,
                mistery_token=my_mistery.mistery_token,
                username=my_mistery.username,
                email=my_mistery.email,
                url=my_mistery.url,
                other=my_mistery.other,
                description=my_mistery.description)
            my_misteries.update({ind: mistery.dict()})

    return my_misteries



@app_read.post(path="/get-mistery-by-title", summary="Here you'll get the misteries by title.", tags=["Misteries"])
def get_mistery_by_title(mistery_title: str = Form(..., max_length=100), token: str = Depends(oauth2_scheme)):
    """
    ***Get Mistery By Title***

    This endpoint let's you get the misteries by writing their title.

    Parameters:
    - ***mistery_title***: Form.
    - ***token***: Depends.

    Returns a set with all the misteries with the same title.

    """
    
    misteries_by_title = local_session.query(PandorasMisteriesDB).filter(PandorasMisteriesDB.mistery_title == mistery_title)
    
    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user_id = user_id_getter(token)

    my_active_misteries_by_title = get_active_misteries(misteries_by_title)

    misteries = {}

    for ind, active_mistery in enumerate(my_active_misteries_by_title, start= 1):
        if active_mistery.foreign_key == int(user_id):
            mistery = MisteryOut(
                mistery_id=active_mistery.mistery_id,
                mistery_title=active_mistery.mistery_title,
                password=active_mistery.password,
                mistery_token=active_mistery.mistery_token,
                username=active_mistery.username,
                email=active_mistery.email,
                description=active_mistery.description,
                url=active_mistery.url,
                other=active_mistery.other
            )
            misteries.update({ind: mistery.dict()})
    return misteries


@app_read.get(
    path="/my-account",
    summary="This endpoint gets the info of a user.",
    tags=["Users"],
    response_model=PandorasUsersOut)
def get_user(token: str = Depends(oauth2_scheme)):
    """
    ***Get User***

    This endpoint gets the users by user_id.

    Parameters:
    - ***token***: Depends.

    Returns the info of the user or an error if users wasn't found.
    """

    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token.")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token.")
    
    user_id = user_id_getter(token)

    user = local_session.query(PandorasUsersDB).filter(PandorasUsersDB.user_id == user_id).first()

    if user:
        return PandorasUsersOut(
            email=user.email,
            username=user.username,
            cellphone=user.cellphone,
            first_name=user.first_name,
            last_name=user.last_name)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
