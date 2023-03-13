from database import Database
import requests
import jsonpickle

# PLAYER_JSON = "https://www.pgatour.com/_next/data/pgatour-prod-1.4.5/en/players.json"

# response = requests.get(PLAYER_JSON)
# data = response.json()['pageProps']['players']['players']


# with open("player_json.json", "w") as file:
#     frozen = jsonpickle.encode(data)
#     file.write(frozen)


with open("player_json.json", "r") as file:
    contents = file.read()
    players = jsonpickle.decode(contents)
    
db = Database()
connection = db.open()
with connection[0] as conn:
    with connection[1] as cur:
        insert_query = """
        INSERT INTO players (pga_id, first_name, last_name, age, headshot_location, country, country_flag) VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """

        for player in players:
            if player.get("isActive"):
                print(player.get("lastName"))
                pga_id = player.get("id")
                first_name = player.get("firstName")
                last_name = player.get("lastName")
                age = int(player.get("playerBio").get("age"))
                head_loc = player.get("headshot")
                country = player.get("country")
                country_flag = player.get("countryFlag")

                data = (pga_id, first_name, last_name, age, head_loc, country, country_flag)
                cur.execute(insert_query, data)
                conn.commit()

db.close()


