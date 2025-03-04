from sqlmodel import SQLModel, Field, String
from pydantic import EmailStr, BaseModel
from typing import Optional

class User(SQLModel, table=True):
  __tablename__ = "users"
  id: int | None = Field(default=None, primary_key=True)
  username: str = Field(String(32), nullable=False, unique=True)
  email: EmailStr = Field(String(64), nullable=False, unique=True)
  password: str = Field(String(128), nullable=False)

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserUpdate(BaseModel):
  username: Optional[str] = None
  password: Optional[str] = None

class UserPublic(BaseModel):
  id: int
  username: str
  email: EmailStr

class UserLogin(BaseModel):
  username: str
  password: str