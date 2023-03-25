import requests
import time
import json
from database import Database

YEARS = ["2013","2014","2015", "2016", "2017", "2018", "2019"]

url = "https://orchestrator.pgatour.com/graphql"

with open("schedule_header.json") as data:
    headers = json.load(data)

for year in YEARS:
    print(f"Running {year} Query")
    payload = f"{{\"query\":\"query Schedule($tourCode: String!, $year: String) {{\\n  schedule(tourCode: $tourCode, year: $year) {{\\n    completed {{\\n      tournaments {{\\n        tournamentName\\n        id\\n        beautyImage\\n        champion\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        championId\\n        city\\n        country\\n        countryCode\\n        courseName\\n        date\\n        dateAccessibilityText\\n        purse\\n        sortDate\\n        startDate\\n        state\\n        stateCode\\n        status {{\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n          roundStatusDisplay\\n        }}\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        tournamentLogo\\n        display\\n        sequenceNumber\\n      }}\\n      month\\n      monthSort\\n      year\\n    }}\\n    seasonYear\\n    tour\\n    seasonYear\\n    upcoming {{\\n      month\\n      year\\n      tournaments {{\\n        id\\n        date\\n        startDate\\n        dateAccessibilityText\\n        tournamentName\\n        tournamentLogo\\n        city\\n        state\\n        stateCode\\n        country\\n        countryCode\\n        courseName\\n        champion\\n        championId\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        beautyImage\\n        status {{\\n          roundStatusDisplay\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n        }}\\n        sortDate\\n        sequenceNumber\\n        purse\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        tournamentLogo\\n        tournamentName\\n        display\\n        sequenceNumber\\n      }}\\n      monthSort\\n    }}\\n    completed {{\\n      month\\n      year\\n      monthSort\\n      tournaments {{\\n        id\\n        date\\n        startDate\\n        dateAccessibilityText\\n        tournamentName\\n        tournamentLogo\\n        city\\n        state\\n        stateCode\\n        country\\n        countryCode\\n        courseName\\n        champion\\n        championId\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        beautyImage\\n        status {{\\n          roundStatusDisplay\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n        }}\\n        sortDate\\n        sequenceNumber\\n        purse\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        display\\n      }}\\n    }}\\n  }}\\n}}\",\"operationName\":\"Schedule\",\"variables\":{{\"tourCode\":\"R\",\"year\":\"{year}\"}}}}"

    response = requests.request("POST", url, data=payload, headers=headers)

    # # print(response.text)

    # with open("2022_schedule.json") as json_data:
    #     all_data = json.load(json_data)
    #     data = all_data['data']['schedule']['completed']
    #     season = all_data['data']['schedule']['seasonYear']    

    all_data = response.json()
    data = all_data['data']['schedule']['completed']
    season = all_data['data']['schedule']['seasonYear'] 

    db = Database()
    connection = db.open()
    with connection[0] as conn:
        with connection[1] as cur:
            insert_query = """
            INSERT INTO tournaments (
                pga_tournament_id,
                tournament_name,
                first_place_earnings,
                purse,
                city,
                country,
                course_name,
                month,
                year,
                season_year            
                ) 
                
            
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            for tournament_month in data:
                month = tournament_month['month']
                year = tournament_month['year']
                for tournament in tournament_month['tournaments']:
                    pga_tournament_id = tournament['id']
                    tournament_name = tournament['tournamentName']
                    first_place_earnings = tournament['championEarnings']
                    purse = tournament['purse']
                    city = tournament['city']
                    country = tournament['country']
                    course = tournament['courseName']

                    data = (
                        pga_tournament_id, 
                        tournament_name, 
                        first_place_earnings, 
                        purse, 
                        city,
                        country, 
                        course,
                        month,
                        year,
                        season
                        )
                    cur.execute(insert_query, data)
                    conn.commit()

    db.close()

    time.sleep(10)