# Here I created the pydantic models for validation.

from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import Optional


class PandorasUsersBase(BaseModel):
    username : str = Field(..., max_length=60)
    password : str = Field(..., max_length=100)


class PandorasUsers(PandorasUsersBase):
    first_name : str = Field(..., max_length=60)
    last_name : str = Field(..., max_length=70)
    email : Optional[EmailStr] = Field(default=None)
    cellphone : Optional[int] = Field(default=None, gt=999999999, lt=10000000000)


class PandorasUserLogin(PandorasUsersBase):
    pass


class PandorasUserUpdate(BaseModel):
    email : Optional[EmailStr] = Field(default=None)
    username : Optional[str] = Field(default=None, max_length=60)
    cellphone : Optional[int] = Field(default=None, gt=999999999, lt=10000000000)


# This one will be the output we can user to the users.
class PandorasUsersOut(PandorasUserUpdate):
    email: Optional[EmailStr] = Field(default=None)
    first_name: str = Field(...)
    last_name: str = Field(...)
    

class MisteryBase(BaseModel):
    mistery_title : str = Field(..., max_length=100)
    password : str = Field(..., max_length=100)
    mistery_token : Optional[str] = Field(default=None, max_length=250)
    username: Optional[str] = Field(default=None, max_length=70)
    email : Optional[EmailStr] = Field(default=None)
    description : Optional[str] = Field(default=None, max_length=300)
    url : Optional[AnyUrl] = Field(default=None)
    other : Optional[str] = Field(default=None, max_length=200)


#class MisteryAll(MisteryBase):
#    foreign_key: int = Field(...)


class MisteryUpdate(BaseModel):
    mistery_name : Optional[str] = Field(default=None, max_length=100)
    password : Optional[str] = Field(default=None, max_length=100)
    mistery_token : Optional[str] = Field(default=None, max_length=250)
    username: Optional[str] = Field(default=None, max_length=70)
    email : Optional[EmailStr] = Field(default=None)
    description : Optional[str] = Field(default=None, max_length=300)
    url : Optional[AnyUrl] = Field(default=None)
    other : Optional[str] = Field(default=None, max_length=200)


class MisteryOut(BaseModel):
    mistery_id : int = Field(...)
    mistery_title : Optional[str] = Field(default=None, max_length=100)
    password : Optional[str] = Field(default=None, max_length=100)
    mistery_token : Optional[str] = Field(default=None, max_length=250)
    username: Optional[str] = Field(default=None, max_length=70)
    email : Optional[EmailStr] = Field(default=None)
    description : Optional[str] = Field(default=None, max_length=300)
    url : Optional[AnyUrl] = Field(default=None)
    other : Optional[str] = Field(default=None, max_length=200)
