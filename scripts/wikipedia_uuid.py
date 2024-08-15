from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import logging, uuid

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# print(soup.get_text())

def fetchPage(url):
    return requests.get(url)

response = fetchPage("https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films")

soup = bs(response.content, features="html.parser")

trs = soup.find("table", class_="wikitable").find("tbody").find_all("tr")

movies = []

for tr in trs:
    tds = tr.find_all("td")
    
    id = uuid.uuid4()
    film = tr.contents[1].text.strip()
    year = tr.contents[3].text.strip()
    awards = tr.contents[5].text.strip()
    nominations = tr.contents[7].text.strip()
    
    movies.append([id, film,year,awards,nominations])
    
df = pd.DataFrame(movies, columns=["Id", "Film", "Year", "Awards", "Nominations"])
print(df)

