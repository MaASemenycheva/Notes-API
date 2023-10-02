from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]


    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"maria",
                "email":"mariasemenycheva@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }


class Settings(BaseModel):
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_secret_key: str = 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'

class LoginModel(BaseModel):
    username:str
    password:str

class Pagination(BaseModel):
    windowSize:int
    page:int


class NoteModel(BaseModel):
    id:Optional[int]
    quantity:int
    note_status:Optional[str]="PENDING"
    note_data:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "note_data":"Something data"
            }
        }


class NoteStatusModel(BaseModel):
    note_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "note_status":"PENDING"
            }
        }