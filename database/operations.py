from sqlalchemy import inspect, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import engine, Base, Session
from .schema import AcademyAwardWinningFilms, TestTable
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_schema():
    try:
        metadata = MetaData()
        
        # Explicitly define tables
        Table('academy_award_winning_films', metadata,
              *[c.copy() for c in AcademyAwardWinningFilms.__table__.columns])
        Table('TestTable', metadata,
              *[c.copy() for c in TestTable.__table__.columns])
        
        # Create tables
        metadata.create_all(engine)
        
        logging.info("Database schema initialized successfully.")
        
        # Verify tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logging.info(f"Tables in the database: {tables}")
        
        if 'academy_award_winning_films' in tables and 'TestTable' in tables:
            logging.info("All required tables have been created successfully.")
        else:
            logging.error("Not all required tables were created.")
            
    except SQLAlchemyError as e:
        logging.error(f"Error initializing database schema: {str(e)}")
        raise

def check_tables_exist():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return 'academy_award_winning_films' in tables and 'TestTable' in tables

def insert_records(session, records):
    try:
        session.add_all(records)
        session.commit()
        logging.info(f"{len(records)} records inserted successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error inserting records: {str(e)}")
        raise

def initDB(records):
    try:
        # Initialize the schema first
        initialize_schema()
        
        # Check if tables exist
        if not check_tables_exist():
            logging.error("Tables were not created successfully.")
            return
        
        session = Session()
        try:
            insert_records(session, records)
        finally:
            session.close()
    except Exception as e:
        logging.error(f"An unexpected error occurred during database initialization: {str(e)}")
        raise

def insertRow(row):
    if not check_tables_exist():
        logging.error("Tables do not exist. Cannot insert row.")
        return

    session = Session()
    try:
        session.add(row)
        session.commit()
        logging.info(f"Row inserted successfully into {row.__tablename__}.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error inserting row into {row.__tablename__}: {str(e)}")
        raise
    finally:
        session.close()