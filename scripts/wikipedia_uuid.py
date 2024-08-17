from bs4 import BeautifulSoup as bs
import requests
import logging
import uuid
from dataframe_functions import exportToCsv, exportToJson, pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetchPage(url):
    try:
        res = requests.get(url)
        logging.info("successfully fetched the page")
        return res
    except:
        logging.error("Failed to fetch the page - No internet connection.")
        raise Exception("Failed to fetch the page - No internet connection.")
        

response = fetchPage("https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films")

# wrong page for testing
# response = fetchPage("https://tedboy.github.io/bs4_doc/4_kind_of_objects.html#beautifulsoup")

soup = bs(response.content, features="html.parser")
logging.info("created the soup")

try: 
    trs = soup.find("table", class_="wikitable").find("tbody").find_all("tr")
    logging.info("successfully found elements in the soup")
except:
    logging.error("Page structure has changed. Unable find specified tags.")
    raise Exception("Page structure has changed. Unable find specified tags.")

movies = []
for tr in trs:
    tds = tr.find_all("td")
    if len(tds) >= 4:  # Ensure the row has enough columns
        id = uuid.uuid4()
        film = tds[0].text.strip()
        year = tds[1].text.strip()
        awards = tds[2].text.strip()
        nominations = tds[3].text.strip()
        movies.append([id, film, year, awards, nominations])
    else:
        logging.error("Didn't manage to find 4 necessary columns in the row")

df = pd.DataFrame(movies, columns=["id", "film", "year", "awards", "nominations"])

# Print only the first 5 records
print(df.head().to_string(index=False))

exportToCsv(df)
exportToJson(df)

    