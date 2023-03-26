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

years_active = []
with open("player_results_by_year.json") as data:
    all_data = json.load(data)

tour_list = all_data['data']['playerProfileSeasonResults']['seasonPills']
for tour in tour_list:
    if tour.get("tourCode") == "R":
        for year in tour.get("years"):
            years_active.append(year.get("year"))

# print(years_active)

# url = "https://orchestrator.pgatour.com/graphql"
# querystring = {"":""}
# payload = f"{{\"query\":\"\\tquery PlayerProfileSeasonResults($playerId: ID!, $tourCode: TourCode, $year: Int) {{\\n  playerProfileSeasonResults(\\n    playerId: $playerId\\n    tourCode: $tourCode\\n    year: $year\\n  ) {{\\n    playerId\\n    tour\\n    displayYear\\n    year\\n    events\\n    wins\\n    top10\\n    top25\\n    cutsMade\\n    missedCuts\\n    withdrew\\n    runnerUp\\n    seasonPills {{\\n      tourCode\\n      years {{\\n        year\\n        displaySeason\\n      }}\\n    }}\\n    cupRank\\n    cupPoints\\n    cupName\\n    cupLogo\\n    cupLogoDark\\n    cupLogoAccessibilityText\\n    rankLogo\\n    rankLogoDark\\n    rankLogoAccessibilityText\\n    officialMoney\\n    tournaments {{\\n      tournamentId\\n      tournamentEndDate\\n      tournamentName\\n      finishPosition\\n      r1\\n      r2\\n      r3\\n      r4\\n      r5\\n      total\\n      toPar\\n      pointsRank\\n      points\\n      tourcastURL\\n      tourcastURLWeb\\n    }}\\n    seasonRecap {{\\n      tourCode\\n      displayMostRecentSeason\\n      mostRecentRecapYear\\n      items {{\\n        year\\n        displaySeason\\n        items {{\\n          tournamentId\\n          year\\n          title\\n          body\\n        }}\\n      }}\\n    }}\\n    amateurHighlights\\n    tourcastEligible\\n  }}\\n}}\\n\\n\\n\\t\",\"operationName\":\"PlayerProfileSeasonResults\",\"variables\":{{\"playerId\":\"35450\",\"tourCode\":\"R\",\"year\":{years_active[0]}}}}}"
# headers = {
#     "authority": "orchestrator.pgatour.com",
#     "accept": "*/*",
#     "accept-language": "en-US,en;q=0.9",
#     "content-type": "application/json",
#     "dnt": "1",
#     "origin": "https://www.pgatour.com",
#     "referer": "https://www.pgatour.com/",
#     "sec-ch-ua": "^\^Google",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "^\^Windows^^",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
#     "x-amz-user-agent": "aws-amplify/3.0.7",
#     "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4",
#     "x-pgat-platform": "web"
# }

# response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

# print(response.json())

db = Database()
connection = db.open()
with connection[0] as conn:
    with connection[1] as cur:
        player_id_select = """
        SELECT id FROM players WHERE pga_id = %s
        
        """
        query_id = all_data['data']['playerProfileSeasonResults']['playerId']
        cur.execute(player_id_select, (query_id,))
        result = cur.fetchone()
        player_id = result.get("id")
        
        insert_query = """
        INSERT INTO player_results (
            player_id,
	        tournament_id,
            tournament_end_date,
            finish_position,
            r1,
	        r2,
	        r3,
	        r4,
            total,
            to_par,
            points_rank,
	        tournament_points
            ) 
              
        VALUES
        (%s, %s, to_date(%s, 'MM.DD.YYYY'), %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        tournaments = all_data['data']['playerProfileSeasonResults']['tournaments']
        for tournament in tournaments:
            pga_tournament_id = tournament['tournamentId']

            tournament_id_select = """
                SELECT id FROM tournaments WHERE pga_tournament_id = %s
            """
            cur.execute(tournament_id_select, (pga_tournament_id,))
            result = cur.fetchone()
            tournament_id = result.get("id")
            
            tournament_end_date = tournament['tournamentEndDate']
            finish_position = tournament['finishPosition']
            
            r1 = tournament['r1'] if tournament['r1'] != "-" else None
            r2 = tournament['r2'] if tournament['r2'] != "-" else None
            r3 = tournament['r3'] if tournament['r3'] != "-" else None
            r4 = tournament['r4'] if tournament['r4'] != "-" else None
            total = tournament['total'] if tournament['total'] != "" else None
            to_par = tournament['toPar']
            points_rank = tournament['pointsRank'] if tournament['pointsRank'] != "-" else None
            tournament_points = tournament['points'] if tournament['points'] != "-" else None

            data_completed = (
                player_id, 
                tournament_id,
                tournament_end_date, 
                finish_position, 
                r1, 
                r2,
                r3,
                r4, 
                total,
                to_par,
                points_rank,
                tournament_points
                )
            cur.execute(insert_query, data_completed)
            conn.commit()

db.close()