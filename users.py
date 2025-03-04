from fastapi import APIRouter, HTTPException, status, Depends
from models import User, UserPublic, UserUpdate
from sqlmodel import Session, select
from db import mydb
from bcrypt import hashpw, gensalt
from auth import get_current_user


router = APIRouter(tags=["users"])

@router.get("/users", status_code=status.HTTP_201_CREATED)
def get_users() -> list[UserPublic]:
  with Session(mydb) as session:
    statement = select(User)
    users = session.exec(statement).fetchall()
    return users

@router.get("/users/{id}", status_code=status.HTTP_200_OK)
def get_users(id: int) -> UserPublic:
  with Session(mydb) as session:
    statement = select(User).where(User.id == id)
    user = session.exec(statement).one_or_none()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
  return user

@router.delete("/users/{id}")
def delete_users(id: int, current_user_id: int = Depends(get_current_user)):
  if current_user_id != id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have permission to delete this user")
  with Session(mydb) as session:
    statement = select(User).where(User.id == current_user_id)
    userExists = session.exec(statement).one_or_none()
    if not userExists:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    session.delete(userExists)
    session.commit()
    return {"message": "User successfully deleted"}
  
@router.put("/users/{id}")
def update_users(id: int, user: UserUpdate, current_user_id: int = Depends(get_current_user)) -> UserPublic:
  if current_user_id != id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this user")
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

