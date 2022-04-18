# This module will be in charge of deactivating users as well as misteries.
 
from fastapi import APIRouter, HTTPException, status, Path, Depends
from config.db_config import local_session
from schemas.db_models import PandorasUsersDB, PandorasMisteriesDB
from jose import jwt, exceptions
from security.authentication_paths import oauth2_scheme, user_id_getter
from security.jwt_handler import ALGORITHM, SECRET_KEY


app_delete = APIRouter()


@app_delete.delete(path="/delete-my-account", summary="This post we'll deactivate users.", tags=["Users"])
def delete_user(token: str = Depends(oauth2_scheme)):
    """
    ***Delete User***

    This endpoint is in charge of deactivating a user.

    Parameters:
    - ***token***: Depends. The token has the user_id as the sub.

    Returns a dictionary message saying the user was deleted or an HTTP error.
    """

    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    all_active_users = local_session.query(PandorasUsersDB).filter(PandorasUsersDB.disabled == False)

    user_id = user_id_getter(token)

    for active_user in all_active_users:
        if active_user.user_id == int(user_id):
            active_user.disabled = True
            return {"Status": f"User {active_user.username} has been deleted."}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


@app_delete.delete(
    path="/delete-mistery/{mistery_id}",
    summary="This endpoint will be in charge of deactivating a mistery.",
    tags=["Misteries"])
def delete_mistery(mistery_id: int = Path(...), token: str = Depends(oauth2_scheme)):
    """
    ***Delete Mistery***

    This endpoint is in charge of deactivating misteries.

    Parameters:
    - ***mistery_id***: Path. To identify the specific mistery.
    - ***token***: Depends. The token payload has the user_id as sub.

    Returns a confirmation message that the mistery was deleted or a not found HTTPException.
    """
    try:
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    mistery_to_deactivate = local_session.query(PandorasMisteriesDB).filter(PandorasMisteriesDB.mistery_id == mistery_id).first()

    if not mistery_to_deactivate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mistery Not Found.")

    mistery_to_deactivate.disabled = True

    return {"Status": f"Mistery {mistery_id} Was Deleted."}
