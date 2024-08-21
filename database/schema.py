from sqlalchemy import Column, String, Integer, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AcademyAwardWinningFilms(Base):
    __tablename__ = 'academy_award_winning_films'
    id = Column(String(36), primary_key=True)
    film = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    awards = Column(Integer, nullable=True)
    nominations = Column(Integer, nullable=True)
    
    __table_args__ = (
        CheckConstraint('year >= 1888', name='check_year'),
    )

    def __init__(self, id: str, film: str, year=None, awards=None, nominations=None):
        self.id = id
        self.film = film
        self.year = year
        self.awards = awards
        self.nominations = nominations

class TestTable(Base):
    __tablename__ = 'TestTable'
    id = Column(String(36), primary_key=True)
    text = Column(String(255), nullable=False)

    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text