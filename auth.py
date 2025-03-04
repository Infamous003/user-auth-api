from bcrypt import hashpw, gensalt, checkpw
import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, User, UserLogin
from sqlmodel import Session, select
from db import mydb
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv

load_dotenv()

# SECRET_KEY = "keep_this_a_secret_please"
# ALGORITHM = "HS256"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["uid"]
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
  
# def verify_token(id: int, token: str = Depends(oauth2_scheme)):
#   payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#   if payload.get("id") != id:
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden access")

# @router.get("/protected")
# def protected_route(user: str = Depends(get_current_user)):
#   return {"message": "Access granted", "user": user}


@router.post("/register")
def register_user(user: UserCreate):
  with Session(mydb) as session:
    query = select(User).where(User.username == user.username)
    user_exists = session.exec(query).first()

    if user_exists:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is already taken")
    
    user.password = hashpw(user.password.encode("utf-8"), gensalt())
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    return {"message": "User successfully created"}
  
# using OAuth2PasswordRequestForm makes it so that we send in the data from the form instead of the request body. the user object is a dictionary and it has keys like, username, and password
@router.post("/login")
# def login(user: UserLogin):
def login(user: OAuth2PasswordRequestForm = Depends()):
  # print(user.client_id, user.client_secret, user.username, user.scopes, "\n--------------------------------------") these are all the keys that the user object has
  with Session(mydb) as session:
    query = select(User).where(User.username == user.username)
    user_exists = session.exec(query).first()
    
    if not user_exists:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")

    if not checkpw(user.password.encode("utf-8"), user_exists.password):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
    
    expiration = datetime.utcnow() + timedelta(minutes=60)
    token = jwt.encode({"uid": user_exists.id, "sub": user_exists.username, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


# @router.put("/users/{id}")
# def update_users(id: int, token: str ,user: UserUpdate) -> UserPublic:
  with Session(mydb) as session:
    statement = select(User).where(User.id == id)
    userExists = session.exec(statement).one_or_none()

  if not userExists:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
  if (user.username): userExists.username = user.username
  if (user.password): userExists.password = hashpw(user.password.encode("utf-8"), gensalt())

  session.add(userExists)
  session.commit()
  session.refresh(userExists)
  return userExists