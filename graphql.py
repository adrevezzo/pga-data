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

    def __generate_payload(self, scrape_type, *args, **kwargs):    
        payload_dict = {
            'stats' : f"{{\"query\":\"query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {{\\n  statDetails(\\n    tourCode: $tourCode\\n    statId: $statId\\n    year: $year\\n    eventQuery: $eventQuery\\n  ) {{\\n    tourCode\\n    year\\n    displaySeason\\n    statId\\n    statType\\n    tournamentPills {{\\n      tournamentId\\n      displayName\\n    }}\\n    yearPills {{\\n      year\\n      displaySeason\\n    }}\\n    statTitle\\n    statDescription\\n    tourAvg\\n    lastProcessed\\n    statHeaders\\n    statCategories {{\\n      category\\n      displayName\\n      subCategories {{\\n        displayName\\n        stats {{\\n          statId\\n          statTitle\\n        }}\\n      }}\\n    }}\\n    rows {{\\n      ... on StatDetailsPlayer {{\\n        __typename\\n        playerId\\n        playerName\\n        country\\n        countryFlag\\n        rank\\n        rankDiff\\n        rankChangeTendency\\n        stats {{\\n          statName\\n          statValue\\n          color\\n        }}\\n      }}\\n      ... on StatDetailTourAvg {{\\n        __typename\\n        displayName\\n        value\\n      }}\\n    }}\\n    sponsorLogo\\n  }}\\n}}\",\"operationName\":\"StatDetails\",\"variables\":{{\"tourCode\":\"R\",\"statId\":\"{kwargs['stat_id']}\",\"year\":{kwargs['schedule_year']},\"eventQuery\":{{\"queryType\":\"{kwargs['query_type'].upper()}\",\"tournamentId\":\"{kwargs['pga_tournament_id']}\"}}}}}}" 


        }   
               
        
        self.payload = payload_dict.get(scrape_type)

    def scrape_stats(self, stat_id: str, schedule_year: int, pga_tournament_id: str, through_event_flag: bool = True):
        if through_event_flag:
            through_event_flag = "THROUGH_EVENT"
        else:
            through_event_flag = "EVENT_ONLY"
        
        self.__generate_payload('stats', stat_id=stat_id, schedule_year=schedule_year, query_type=through_event_flag, pga_tournament_id=pga_tournament_id)
        self.__make_connection()
        
        return self.response.json()
    

gql = GraphQLQuery()
results = gql.scrape_stats(stat_id="02675", schedule_year=2023, through_event_flag="THROUGH_EVENT", pga_tournament_id="R2013007")
print(results)