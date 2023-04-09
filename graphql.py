import json
import requests

class GraphQLQuery:
    def __init__(self) -> None:
        with open("graphql_headers.json") as header_file:
            self.headers = json.load(header_file)
        
        self.payload = None
        self.url = "https://orchestrator.pgatour.com/graphql"
        self.response = None

    
    def __make_connection(self):
        self.response = requests.request("POST", self.url, data=self.payload, headers=self.headers)

   
    def __generate_payload(self, scrape_type, stat_id = None, schedule_year = None, pga_tournament_id = None, query_type = None):    
        payload_dict = {
            'stats' : f"{{\"query\":\"query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {{\\n  statDetails(\\n    tourCode: $tourCode\\n    statId: $statId\\n    year: $year\\n    eventQuery: $eventQuery\\n  ) {{\\n    tourCode\\n    year\\n    displaySeason\\n    statId\\n    statType\\n    tournamentPills {{\\n      tournamentId\\n      displayName\\n    }}\\n    yearPills {{\\n      year\\n      displaySeason\\n    }}\\n    statTitle\\n    statDescription\\n    tourAvg\\n    lastProcessed\\n    statHeaders\\n    statCategories {{\\n      category\\n      displayName\\n      subCategories {{\\n        displayName\\n        stats {{\\n          statId\\n          statTitle\\n        }}\\n      }}\\n    }}\\n    rows {{\\n      ... on StatDetailsPlayer {{\\n        __typename\\n        playerId\\n        playerName\\n        country\\n        countryFlag\\n        rank\\n        rankDiff\\n        rankChangeTendency\\n        stats {{\\n          statName\\n          statValue\\n          color\\n        }}\\n      }}\\n      ... on StatDetailTourAvg {{\\n        __typename\\n        displayName\\n        value\\n      }}\\n    }}\\n    sponsorLogo\\n  }}\\n}}\",\"operationName\":\"StatDetails\",\"variables\":{{\"tourCode\":\"R\",\"statId\":\"{stat_id}\",\"year\":{schedule_year},\"eventQuery\":{{\"queryType\":\"{query_type}\",\"tournamentId\":\"{pga_tournament_id}\"}}}}}}" ,
            'schedule' : f"{{\"query\":\"query Schedule($tourCode: String!, $year: String) {{\\n  schedule(tourCode: $tourCode, year: $year) {{\\n    completed {{\\n      tournaments {{\\n        tournamentName\\n        id\\n        beautyImage\\n        champion\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        championId\\n        city\\n        country\\n        countryCode\\n        courseName\\n        date\\n        dateAccessibilityText\\n        purse\\n        sortDate\\n        startDate\\n        state\\n        stateCode\\n        status {{\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n          roundStatusDisplay\\n        }}\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        tournamentLogo\\n        display\\n        sequenceNumber\\n      }}\\n      month\\n      monthSort\\n      year\\n    }}\\n    seasonYear\\n    tour\\n    seasonYear\\n    upcoming {{\\n      month\\n      year\\n      tournaments {{\\n        id\\n        date\\n        startDate\\n        dateAccessibilityText\\n        tournamentName\\n        tournamentLogo\\n        city\\n        state\\n        stateCode\\n        country\\n        countryCode\\n        courseName\\n        champion\\n        championId\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        beautyImage\\n        status {{\\n          roundStatusDisplay\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n        }}\\n        sortDate\\n        sequenceNumber\\n        purse\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        tournamentLogo\\n        tournamentName\\n        display\\n        sequenceNumber\\n      }}\\n      monthSort\\n    }}\\n    completed {{\\n      month\\n      year\\n      monthSort\\n      tournaments {{\\n        id\\n        date\\n        startDate\\n        dateAccessibilityText\\n        tournamentName\\n        tournamentLogo\\n        city\\n        state\\n        stateCode\\n        country\\n        countryCode\\n        courseName\\n        champion\\n        championId\\n        champions {{\\n          displayName\\n          playerId\\n        }}\\n        championEarnings\\n        beautyImage\\n        status {{\\n          roundStatusDisplay\\n          roundDisplay\\n          roundStatus\\n          roundStatusColor\\n        }}\\n        sortDate\\n        sequenceNumber\\n        purse\\n        ticketsURL\\n        tourStandingHeading\\n        tourStandingValue\\n        display\\n      }}\\n    }}\\n  }}\\n}}\",\"operationName\":\"Schedule\",\"variables\":{{\"tourCode\":\"R\",\"year\":\"{schedule_year}\"}}}}"

        }   
               
        
        self.payload = payload_dict.get(scrape_type)

    
    def scrape_stats(self, stat_id: str, schedule_year: int, pga_tournament_id: str, through_event_flag: bool = True):
        if through_event_flag:
            through_event_flag = "THROUGH_EVENT"
        else:
            through_event_flag = "EVENT_ONLY"
        
        self.__generate_payload('stats', stat_id=stat_id, schedule_year=schedule_year, query_type=through_event_flag.upper(), pga_tournament_id=pga_tournament_id)
        self.__make_connection()
        
        return self.response.json()
    

    def scrape_schedule(self, schedule_year: int):      
        self.__generate_payload('schedule', schedule_year=schedule_year)
        self.__make_connection()
        
        return self.response.json()
    




# gql = GraphQLQuery()
# results = gql.scrape_schedule(schedule_year=2023)
# print(results)