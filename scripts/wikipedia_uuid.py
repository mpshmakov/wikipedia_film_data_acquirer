"""
Wikipedia Oscar-winning films scraper and database population script.

This script scrapes data about Academy Award-winning films from Wikipedia,
stores it in a database, and exports it to CSV and JSON formats.
"""

import uuid
import logging
import pandas as pd
from wiki import BeautifulSoup as bs, requests, fetchPage
from wiki.export_functions import exportToCsv, exportToJson
from database import initDB, insertRow, AcademyAwardWinningFilms, TestTable, Session
from database.operations import initialize_schema, check_tables_exist
from sqlalchemy.exc import SQLAlchemyError
from wiki.utils import clean_numeric


def scrape_oscar_winning_films():
    """
    Scrape Oscar-winning films data from Wikipedia.

    Returns:
        list: A list of tuples containing film data (id, film, year, awards, nominations).

    Raises:
        Exception: If the page structure has changed and data cannot be scraped.
    """
    url = "https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films"
    response = fetchPage(url)
    print(response.content) # to see if return_value of the fetchPage changes when i test this function
    soup = bs(response.content, features="html.parser")
    logging.info("Created the soup.")

    try:
        trs = soup.find("table", class_="wikitable").find("tbody").find_all("tr")
        logging.info("Successfully found elements in the soup.")
    except AttributeError:
        logging.error("Page structure has changed. Unable to find specified tags.")
        raise Exception("Page structure has changed. Unable to find specified tags.")

    movies = []
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) >= 4:  # Ensure the row has enough columns
            id = str(uuid.uuid4())
            film = tds[0].text.strip()
            year = clean_numeric(tds[1].text.strip())
            awards = clean_numeric(tds[2].text.strip())
            nominations = clean_numeric(tds[3].text.strip())
            movies.append((id, film, year, awards, nominations))
        else:
            logging.warning("Didn't manage to find 4 necessary columns in the row.")
    
    return movies


def main():
    """
    Main function to orchestrate the scraping, database population, and data export process.
    """
    try:
        # Initialize the database schema
        initialize_schema()

        # Verify tables exist
        if not check_tables_exist():
            logging.error("Tables do not exist after schema initialization. Exiting.")
            return

        movies_data = scrape_oscar_winning_films()

        # Create AcademyAwardWinningFilms objects
        movies = [AcademyAwardWinningFilms(*movie) for movie in movies_data]

        # Initialize the database and insert all movies
        initDB(movies)

        # Verify tables exist again
        if not check_tables_exist():
            logging.error("Tables do not exist after initDB. Exiting.")
            return

        # Test inserting individual rows
        new_film = AcademyAwardWinningFilms(str(uuid.uuid4()), "Test Film", 2023, 1, 5)
        new_test = TestTable(str(uuid.uuid4()), "Test entry")
        insertRow(new_film)
        print("Inserted new film.")
        insertRow(new_test)
        print("Inserted test entry.")

        # Create DataFrame for CSV and JSON export
        df = pd.DataFrame(movies_data, columns=["id", "film", "year", "awards", "nominations"])
        exportToCsv(df)
        exportToJson(df)
        print("CSV and JSON files created successfully.")

    except SQLAlchemyError as e:
        logging.error(f"A database error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
