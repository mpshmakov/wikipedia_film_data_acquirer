from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import logging

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# print(soup.get_text())

def fetchPage(url):
    return requests.get(url)

response = fetchPage("https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films")

soup = bs(response.content, features="html.parser")

trs = soup.find("table", class_="wikitable").find("tbody").find_all("tr")

movies = []

id = -1
for tr in trs:
    tds = tr.find_all("td")
    
    id += 1
    film = tr.contents[1].text
    year = tr.contents[3].text
    awards = tr.contents[5].text
    nominations = tr.contents[7].text
    
    movies.append([id, film,year,awards,nominations])
    
df = pd.DataFrame(movies, columns=["Id", "Film", "Year", "Awards", "Nominations"])
print(df)

