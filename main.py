# Here we'll include all the endpoints.

from fastapi import FastAPI
from routes.create import app_create
from routes.read import app_read
from routes.update import app_update
from routes.delete import app_delete
from security.authentication_paths import app_authentication

app = FastAPI()
app.include_router(app_create)
app.include_router(app_read)
app.include_router(app_update)
app.include_router(app_delete)
app.include_router(app_authentication)


@app.get(path="/", summary="This endpoint will explain people what this api is all about.", tags=["Home"])
def welcome():
    return {"Pandora's Box": "This is an API creted to help you save and keep your passwordsS"}

