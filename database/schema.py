# db should be in data folder (wiki_films.db)

from sqlalchemy import Column, String, Integer, create_engine, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Films(Base):
    __tablename__ = 'Films'

    id = Column(String(36), primary_key=True)
    film = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    awards = Column(Integer, nullable=True)
    nominations = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('year >= 1888', name='check_year'),
    )

    def __init__(self, id: str, film: str, year="NULL", awards="NULL", nominations="NULL"):
        self.id = id
        self.film = film
        self.year = year
        self.awards = awards
        self.nominations = nominations

class TestTable(Base):
    __tablename__ = 'TestTable'

    id = Column(String(36), primary_key=True)
    text = Column(String(255), nullable=False)

    def __init__(self, id:str, text:str):
        self.id = id
        self.text = text
