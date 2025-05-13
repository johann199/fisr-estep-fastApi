from fastapi import APIRouter
from fastapi.responses import  JSONResponse
from pydantic import BaseModel
from user_jwt import crearToken


routerUser = APIRouter()
class User(BaseModel):
    email: str
    password: str


@routerUser.post("/login", tags=["autenticacion"])
def login(user:User):
    if user.email == "johann@gmail.com" and user.password == "1234":
        token: str = crearToken(user.dict())
        print(token)
        return JSONResponse(content={"message": "Login successful", "token": token}, status_code=200)

