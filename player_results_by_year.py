from database import Database
import time
import requests
from bs4 import BeautifulSoup
import re
import json

# Static data for testing
# with open("player_results_by_year.json") as data:
#     all_data = json.load(data)

db = Database()
connection = db.open()
with connection[0] as conn:
    with connection[1] as cur:
        get_players_query = """
        SELECT 
        first_name || ' ' || last_name as player_name
        ,pga_id 
        FROM players
        """
        cur.execute(get_players_query)
        results = cur.fetchall()

db.close()

all_players = [(result.get("pga_id"),result.get("player_name")) for result in results]


url = "https://orchestrator.pgatour.com/graphql"
querystring = {"":""}
with open("player_results_header.json") as data_completed:
    headers = json.load(data_completed)

for player in all_players[30:100]:
    payload = f"{{\"query\":\"\\tquery PlayerProfileSeasonResults($playerId: ID!, $tourCode: TourCode, $year: Int) {{\\n  playerProfileSeasonResults(\\n    playerId: $playerId\\n    tourCode: $tourCode\\n    year: $year\\n  ) {{\\n    playerId\\n    tour\\n    displayYear\\n    year\\n    events\\n    wins\\n    top10\\n    top25\\n    cutsMade\\n    missedCuts\\n    withdrew\\n    runnerUp\\n    seasonPills {{\\n      tourCode\\n      years {{\\n        year\\n        displaySeason\\n      }}\\n    }}\\n    cupRank\\n    cupPoints\\n    cupName\\n    cupLogo\\n    cupLogoDark\\n    cupLogoAccessibilityText\\n    rankLogo\\n    rankLogoDark\\n    rankLogoAccessibilityText\\n    officialMoney\\n    tournaments {{\\n      tournamentId\\n      tournamentEndDate\\n      tournamentName\\n      finishPosition\\n      r1\\n      r2\\n      r3\\n      r4\\n      r5\\n      total\\n      toPar\\n      pointsRank\\n      points\\n      tourcastURL\\n      tourcastURLWeb\\n    }}\\n    seasonRecap {{\\n      tourCode\\n      displayMostRecentSeason\\n      mostRecentRecapYear\\n      items {{\\n        year\\n        displaySeason\\n        items {{\\n          tournamentId\\n          year\\n          title\\n          body\\n        }}\\n      }}\\n    }}\\n    amateurHighlights\\n    tourcastEligible\\n  }}\\n}}\\n\\n\\n\\t\",\"operationName\":\"PlayerProfileSeasonResults\",\"variables\":{{\"playerId\":\"{player[0]}\",\"tourCode\":\"R\",\"year\":2023}}}}"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    all_data = response.json()

    years_active = []
    tour_list = all_data['data']['playerProfileSeasonResults']['seasonPills']
    for tour in tour_list:
        if tour.get("tourCode") == "R":
            for year in tour.get("years"):
                years_active.append(year.get("year"))
    
    time.sleep(10)

    
    for year in years_active:
        if int(year) <2013:
            print(f"Player: {player[1]}, Year: {year} - skipping")
            continue
        else:
            print(f"Player: {player[1]}, Year: {year}")

            payload = f"{{\"query\":\"\\tquery PlayerProfileSeasonResults($playerId: ID!, $tourCode: TourCode, $year: Int) {{\\n  playerProfileSeasonResults(\\n    playerId: $playerId\\n    tourCode: $tourCode\\n    year: $year\\n  ) {{\\n    playerId\\n    tour\\n    displayYear\\n    year\\n    events\\n    wins\\n    top10\\n    top25\\n    cutsMade\\n    missedCuts\\n    withdrew\\n    runnerUp\\n    seasonPills {{\\n      tourCode\\n      years {{\\n        year\\n        displaySeason\\n      }}\\n    }}\\n    cupRank\\n    cupPoints\\n    cupName\\n    cupLogo\\n    cupLogoDark\\n    cupLogoAccessibilityText\\n    rankLogo\\n    rankLogoDark\\n    rankLogoAccessibilityText\\n    officialMoney\\n    tournaments {{\\n      tournamentId\\n      tournamentEndDate\\n      tournamentName\\n      finishPosition\\n      r1\\n      r2\\n      r3\\n      r4\\n      r5\\n      total\\n      toPar\\n      pointsRank\\n      points\\n      tourcastURL\\n      tourcastURLWeb\\n    }}\\n    seasonRecap {{\\n      tourCode\\n      displayMostRecentSeason\\n      mostRecentRecapYear\\n      items {{\\n        year\\n        displaySeason\\n        items {{\\n          tournamentId\\n          year\\n          title\\n          body\\n        }}\\n      }}\\n    }}\\n    amateurHighlights\\n    tourcastEligible\\n  }}\\n}}\\n\\n\\n\\t\",\"operationName\":\"PlayerProfileSeasonResults\",\"variables\":{{\"playerId\":\"{player[0]}\",\"tourCode\":\"R\",\"year\":{year}}}}}"
            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            all_data = response.json()

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
                        
                        if not result:
                            continue
                        else:
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

            time.sleep(10)

    db.close()