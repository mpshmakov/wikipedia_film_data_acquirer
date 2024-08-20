from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .schema import Films, Base, TestTable

engine = create_engine('sqlite:///wiki_films.db')
session = Session(engine)

def initDB():
    Base.metadata.create_all(bind=engine) # this should create the tables
    # newFilm = Films("newidwdddd5ss4dd4", "Cardddseddd4dd4", 19000)
    # session.add(newFilm)
    # session.commit()
    

def insertRow(row: (Films | TestTable)):
    session.add(row)
    session.commit()