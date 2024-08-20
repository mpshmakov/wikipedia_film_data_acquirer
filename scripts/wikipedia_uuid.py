from wiki import BeautifulSoup as bs, requests, logging, uuid, pd, fetchPage, exportToCsv, exportToJson
from database import initDB, insertRow, Films, TestTable

def scrape_oscar_winning_films():
    url = "https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films"
    response = fetchPage(url)
    soup = bs(response.content, features="html.parser")
    logging.info("Created the soup")

    try:
        trs = soup.find("table", class_="wikitable").find("tbody").find_all("tr")
        logging.info("Successfully found elements in the soup")
    except:
        logging.error("Page structure has changed. Unable to find specified tags.")
        raise Exception("Page structure has changed. Unable to find specified tags.")

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

    return pd.DataFrame(movies, columns=["id", "film", "year", "awards", "nominations"])

def main():
    df = scrape_oscar_winning_films()
    
    # Print only the first 5 records
    # print(df.head().to_string(index=False))
    
    # exportToCsv(df)
    # exportToJson(df)
    initDB()
    newFilmRow = Films("asdf33dddd33", "plssaddnes", 3000)
    newTestRow = TestTable("slsldsls", "some text")

    ## test that the funciton doesn't accept any other classes other than the specified ones
    # class Random:
    #     id: int
    #     def __init__(self, id):
    #         self.id = id

    # random = Random(4)
    # insertRow(random)
    # print("inserted random")

    insertRow(newFilmRow)
    print("inserted film")
    insertRow(newTestRow)
    print("inserted test")
    
    

if __name__ == "__main__":
    main()