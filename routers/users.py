from fastapi import APIRouter
from pydantic import BaseModel
from user_jwt import createToken

login_user = APIRouter()

class User(BaseModel):
    email:str
    password: str



@login_user.post('/login', tags=['Authentication'])
def login(user: User):
    if user.email == 'oscar@gmail.com' and user.password=='12345':
        token: str= createToken(user.model_dump())
        print(token)
        return token