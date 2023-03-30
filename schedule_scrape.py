import requests
import time
import json
from database import Database
import queries

YEARS = ["2013","2014","2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
# YEARS = ['2023']
url = "https://orchestrator.pgatour.com/graphql"

with open("schedule_header.json") as data_completed:
    headers = json.load(data_completed)

for year in YEARS:
    print(f"Running {year} Query")
    payload_for_tournament_info = f"{{\"query\":\"query Schedule($tourCode: String!, $year: String) {{\\n  schedule(tourCode: $tourCode, year: $year) {{\\n    completed {{\\n      tournaments {{\\n        tournamentName\\n        id\\n        beautyImage\\n        champion\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        championId\\n        city\\n        country\\n        countryCode\\n        courseName\\n        date\\n        dateAccessibilityText\\n        purse\\n        sortDate\\n        startDate\\n        state\\n        stateCode\\n        status {{\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n          roundStatusDisplay\\n        }}\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        tournamentLogo\\n        display\\n        sequenceNumber\\n      }}\\n      month\\n      monthSort\\n      year\\n    }}\\n    seasonYear\\n    tour\\n    seasonYear\\n    upcoming {{\\n      month\\n      year\\n      tournaments {{\\n        id\\n        date\\n        startDate\\n        dateAccessibilityText\\n        tournamentName\\n        tournamentLogo\\n        city\\n        state\\n        stateCode\\n        country\\n        countryCode\\n        courseName\\n        champion\\n        championId\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        beautyImage\\n        status {{\\n          roundStatusDisplay\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n        }}\\n        sortDate\\n        sequenceNumber\\n        purse\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        tournamentLogo\\n        tournamentName\\n        display\\n        sequenceNumber\\n      }}\\n      monthSort\\n    }}\\n    completed {{\\n      month\\n      year\\n      monthSort\\n      tournaments {{\\n        id\\n        date\\n        startDate\\n        dateAccessibilityText\\n        tournamentName\\n        tournamentLogo\\n        city\\n        state\\n        stateCode\\n        country\\n        countryCode\\n        courseName\\n        champion\\n        championId\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        beautyImage\\n        status {{\\n          roundStatusDisplay\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n        }}\\n        sortDate\\n        sequenceNumber\\n        purse\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        display\\n      }}\\n    }}\\n  }}\\n}}\",\"operationName\":\"Schedule\",\"variables\":{{\"tourCode\":\"R\",\"year\":\"{year}\"}}}}"

    time.sleep(10)
    response = requests.request("POST", url, data=payload_for_tournament_info, headers=headers)

    # with open("2022_schedule.json") as data:
    #     all_data = json.load(data)

    all_data = response.json()

    data_completed = all_data['data']['schedule']['completed']
    data_upcoming = all_data['data']['schedule']['upcoming']
    season = all_data['data']['schedule']['seasonYear']
  
    with Database(db_type='dev') as (con, cur):
        for status in (data_completed, data_upcoming):
            for tournament_month in status:
                month = tournament_month['month']
                year = tournament_month['year']
                for tournament in tournament_month['tournaments']:
                    pga_tournament_id = tournament['id']
                    tournament_name = tournament['tournamentName']
                    tournament_num = (pga_tournament_id[-3:])
                    first_place_earnings = tournament['championEarnings']
                    purse = tournament['purse']
                    city = tournament['city']
                    state = tournament['state']
                    country = tournament['country']
                    course = tournament['courseName']

                    data_completed = (
                        pga_tournament_id, 
                        tournament_name,
                        tournament_num, 
                        first_place_earnings, 
                        purse, 
                        city,
                        state,
                        country, 
                        course,
                        month,
                        year,
                        season
                        )
                    cur.execute(queries.SCHEDULE_INSERT_QUERY, data_completed)
                    con.commit()

    