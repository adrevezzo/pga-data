from database import Database
import requests
import json

# with open("player_dict_header.json") as data_completed:
#     headers = json.load(data_completed)

# url = "https://orchestrator.pgatour.com/graphql"

# payload = "{\"query\":\"query PlayerDirectory($tourCode: TourCode!, $active: Boolean) {\\n  playerDirectory(tourCode: $tourCode, active: $active) {\\n    tourCode\\n    players {\\n      id\\n      isActive\\n      firstName\\n      lastName\\n      shortName\\n      displayName\\n      alphaSort\\n      country\\n      countryFlag\\n      headshot\\n      playerBio {\\n        id\\n        age\\n        education\\n        turnedPro\\n      }\\n    }\\n  }\\n}\",\"operationName\":\"PlayerDirectory\",\"variables\":{\"tourCode\":\"R\"}}"

# response = requests.request("POST", url, data=payload, headers=headers)

# players = response.json()

# with open("player_dictionary.json", "w") as file:
#     json.dump(players, file)

with open("player_dictionary.json") as data_completed:
    players = json.load(data_completed)

with Database(db_type='dev') as (con, cur):
    get_players_query = """
    SELECT 
    first_name || ' ' || last_name as player_name
    ,pga_id 
    
    FROM players
    """
    cur.execute(get_players_query)
    results = cur.fetchall() 
    player_ids = [result.get("pga_id") for result in results]  

    insert_query = """
    INSERT INTO players (pga_id, first_name, last_name, age, headshot_location, country, country_flag) VALUES
    (%s, %s, %s, %s, %s, %s, %s)
    """

    for player in players['data']['playerDirectory']['players']:
        if player.get("id") in list(player_ids):
            print(f"\n{player['firstName']} {player['lastName']} in database")
            continue
        else:     
            if player.get("isActive"):
                print(f"\n{player['firstName']} {player['lastName']} will be added")
                pga_id = player.get("id")
                first_name = player.get("firstName")
                last_name = player.get("lastName")
                age = int(player.get("playerBio").get("age"))
                head_loc = player.get("headshot")
                country = player.get("country")
                country_flag = player.get("countryFlag")

                data = (pga_id, first_name, last_name, age, head_loc, country, country_flag)
                cur.execute(insert_query, data)
                con.commit()

print(con.closed, " ", cur.closed)

