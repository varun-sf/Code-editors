from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from security.hashing import hash_password, verify_password
from security.token import create_access_token
from datetime import timedelta

def signup(username: str, password: str, db: Session):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

def login(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
