"""
Database operations module.

This module provides functions for initializing the database schema,
checking table existence, and inserting records into the database.
"""

from sqlalchemy import inspect, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import engine, Base, Session
from .schema import AcademyAwardWinningFilms, TestTable
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_schema():
    """
    Initialize the database schema by creating required tables.

    Raises:
        SQLAlchemyError: If there's an error during schema initialization.
    """
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
    """
    Check if required tables exist in the database.

    Returns:
        bool: True if all required tables exist, False otherwise.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return 'academy_award_winning_films' in tables and 'TestTable' in tables

def insert_records(session, records):
    """
    Insert multiple records into the database.

    Args:
        session (Session): SQLAlchemy session object.
        records (list): List of record objects to be inserted.

    Raises:
        SQLAlchemyError: If there's an error during record insertion.
    """
    try:
        session.add_all(records)
        session.commit()
        logging.info(f"{len(records)} records inserted successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error inserting records: {str(e)}")
        raise

def initDB(records):
    """
    Initialize the database by creating schema and inserting initial records.

    Args:
        records (list): List of record objects to be inserted after schema creation.

    Raises:
        Exception: If an unexpected error occurs during database initialization.
    """
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
    """
    Insert a single row into the database.

    Args:
        row: The row object to be inserted.

    Raises:
        SQLAlchemyError: If there's an error during row insertion.
    """
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
