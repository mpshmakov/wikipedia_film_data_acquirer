from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import logging
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetchPage(url):
    return requests.get(url)

response = fetchPage("https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films")
soup = bs(response.content, features="html.parser")
trs = soup.find("table", class_="wikitable").find("tbody").find_all("tr")

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

df = pd.DataFrame(movies, columns=["Id", "Film", "Year", "Awards", "Nominations"])

# Print only the first 5 records
print(df.head().to_string(index=False))