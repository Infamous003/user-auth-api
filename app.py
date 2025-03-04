from fastapi import FastAPI
from db import create_tables_and_db
import users
import auth

app = FastAPI()
create_tables_and_db()

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def index():
  return {"data": "Welcome to User API"}
