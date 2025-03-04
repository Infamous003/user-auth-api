from sqlmodel import create_engine, SQLModel

mydb = create_engine("sqlite:///database.db", echo=True)

def create_tables_and_db():
  SQLModel.metadata.create_all(mydb)