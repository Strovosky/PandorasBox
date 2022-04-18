from fastapi import APIRouter, Path, Body, HTTPException, status, Depends
from config.db_config import local_session
from schemas.db_models import PandorasMisteriesDB, PandorasUsersDB
from models.pydantic_models import MisteryOut, MisteryUpdate, PandorasUserUpdate, PandorasUsersOut
from security.authentication_paths import oauth2_scheme, user_id_getter
from jose import jwt, exceptions
from security.jwt_handler import ALGORITHM, SECRET_KEY

app_update = APIRouter()

@app_update.put(
    path="/update_mistery/{mistery_id}",
    summary="This endpoint will let us update a specific mistery.",
    tags=["Misteries"])
def update_mistery(mistery_to_update: MisteryUpdate = Body(...), token: str = Depends(oauth2_scheme), mistery_id: int = Path(...)):
    """
    ***Update Mistery***

    This endpoint let's you update a mistery.

    Parameters:
    - ***token***: Depends. The token's payload has the user_id as sub.
    - ***mistery_to_update***: Body.

    Returns a response model we the info users should see.
    """
    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user_id = user_id_getter(token)

    fk_misteries = local_session.query(PandorasMisteriesDB).filter(PandorasMisteriesDB.foreign_key == user_id)

    if not fk_misteries:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found.")

    for mistery_to_update_db in fk_misteries:
        if not mistery_to_update_db.disabled:
            if mistery_to_update_db.mistery_id == mistery_id:
                if mistery_to_update.mistery_name:
                    mistery_to_update_db.mistery_name = mistery_to_update.mistery_name
                if mistery_to_update.mistery_name:
                    mistery_to_update_db.password = mistery_to_update.password
                if mistery_to_update.mistery_token:
                    mistery_to_update_db.mistery_token = mistery_to_update.mistery_token
                if mistery_to_update.email:
                    mistery_to_update_db.email = mistery_to_update.email
                if mistery_to_update.url:
                    mistery_to_update_db.url = mistery_to_update.url
                if mistery_to_update.username:
                    mistery_to_update_db.username = mistery_to_update.username
                if mistery_to_update.description:
                    mistery_to_update_db.description = mistery_to_update.description
                if mistery_to_update.other:
                    mistery_to_update_db.other = mistery_to_update.other
                return mistery_to_update


@app_update.put(
    path="/update-user/",
    summary="This endpoint let's you update a user.",
    tags=["Users"],
    response_model=PandorasUsersOut)
def update_user(user_update: PandorasUserUpdate = Body(...), token: str = Depends(oauth2_scheme)):
    """
    ***Update User***

    This endpoint will updated a specifi user.

    Parameters:
    - ***token***: Depends. With the user_id as sub in the payload.
    - ***user_update***: PandorasUserUpdate.

    Returns a response model with the info the user should see.
    """

    # Let's first validate the token

    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Signature.")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    user_id = user_id_getter(token)

    user_to_update = local_session.query(PandorasUsersDB).filter(PandorasUsersDB.user_id == user_id).first()

    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    if not user_to_update.disabled:
        if user_update.cellphone:
            user_to_update.cellphone = user_update.cellphone
        if user_update.email:
            user_to_update.email = user_update.email
        if user_update.username:
            user_to_update.username = user_update.username
        
        return PandorasUsersOut(
            email=user_to_update.email,
            username=user_to_update.username,
            cellphone=user_to_update.cellphone,
            first_name=user_to_update.first_name,
            last_name=user_to_update.last_name)
