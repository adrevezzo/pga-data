from database import Database
import time
import requests
from bs4 import BeautifulSoup
import re
import json

def name_clean(name_string):
    name_as_list = [*name_string]
    name = ''
    for i,char in enumerate(name_as_list[::-1]):
        if i == 0 and char == "." or char == ",":
            continue
        else:
            if char == ' ':
                name += "-"
            else:
                name += char
    return name[::-1]


db = Database()
connection = db.open()
with connection[0] as conn:
    with connection[1] as cur:
        query = """
        SELECT pga_id, first_name, last_name FROM players
        """

        cur.execute(query)
        players = cur.fetchall()


db.close()


for player in players:
    pga_id = player.get('pga_id')
    first_name = name_clean(player.get('first_name').lower())
    last_name = name_clean(player.get('last_name').lower()) 
    player_url = f"https://www.pgatour.com/player/{pga_id}/{first_name}-{last_name}/results"
    print(player_url)

    res = requests.get(player_url)

    soup = BeautifulSoup(res.text, "html.parser")
    body = soup.select("#__NEXT_DATA__")[0].get_text()
    json_data = json.loads(body)
    print(body)
    # print(type(soup)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # stuff = soup.find("h1")
    # print(stuff.get_text())

    time.sleep(5)