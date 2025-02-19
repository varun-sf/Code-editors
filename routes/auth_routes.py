from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers.auth_controller import signup, login
from pydantic import BaseModel

router = APIRouter()

class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/signup")
def register_user(user: UserSignup, db: Session = Depends(get_db)):
    return signup(user.username, user.password, db)

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login(user.username, user.password, db)
