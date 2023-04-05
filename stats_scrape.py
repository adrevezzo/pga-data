import requests
import time
import json
from database import Database
import queries
import re
from utils import create_json_file
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor

stat_id_dict = {}

EXTRA_WORDS = ('by', 'measured', '_', '®', 'from', 'the', 'or')

PATTERN_DICT = {
    'NON_ALPHA_PATTERN' : {
        'pattern' : re.compile(r"[:\.,\s,\(,\)']+"),
        'replace_string' : ""
    },

    'APPROACH_PATTERN' : {
        'pattern' : re.compile(r"^[a-zA-Z]pproach[a-zA-Z]*"),
        'replace_string' : 'App'
    },

    'PERCENTAGE_PATTERN' : {
        'pattern' : re.compile(r"^[a-zA-Z]ercent[age]*"),
        'replace_string' : 'Pct'
    },

    'DRIVING_PATTERN' : {
        'pattern' : re.compile(r"^[a-zA-Z]riv[^s]*"),
        'replace_string' : 'Drv'
    },

    'YARDAGE_PATTERN' : {
        'pattern' : re.compile(r"^[a-zA-Z]ard[^s]*"),
        'replace_string' : 'Ydg'
    },
    
    'FAIRWAY_PATTERN' : {
        'pattern' : re.compile(r"^[a-zA-Z]airway[^s]*"),
        'replace_string' : 'Fwy'
    },

    'ROUGH_PATTERN' : { 
        'pattern' : re.compile(r"^[rR]ough"),
        'replace_string' : 'Rgh'
    },

    'BIRDIE_PATTERN' : {
        'pattern' : re.compile(r"[bB]irdie[^s]*"),
        'replace_string' : 'Brd'
    },

    'BOGEY_PATTERN' : {
        'pattern' : re.compile(r"[bB]ogey[^es]*"),
        'replace_string' : 'Bgy'
    },

    'PROXIMITY_PATTERN' : {
        'pattern' : re.compile(r"[pP]roximity"),
        'replace_string' : 'Prox'
    },

    'AVERAGE_PATTERN' : {
        'pattern' : re.compile(r"[aA]verage"),
        'replace_string' : 'Avg'
    },

    'EFFICIENCY_PATTERN' : {
        'pattern' : re.compile(r"[eE]fficiency"),
        'replace_string' : 'Eff'
    },

    'ROUND_PATTERN' : {
        'pattern' : re.compile(r"[rR]oun[^s]*"),
        'replace_string' : 'Rnd'
    },

    'CONSECUTIVE_PATTERN' : {
        'pattern' : re.compile(r"[cC]onsecutive"),
        'replace_string' : 'Cons'
    },

    'AVOIDANCE_PATTERN' : {
        'pattern' : re.compile(r"[aA]voidance"),
        'replace_string' : 'Avoid'
    },

    'PUTTING_PATTERN' : {
        'pattern' : re.compile(r"[pP]utting"),
        'replace_string' : 'Putt'
    },

    'DISTANCE_PATTERN' : {
        'pattern' : re.compile(r"[dD]istance"),
        'replace_string' : 'Dist'
    },

    'SCORING_PATTERN' : {
        'pattern' : re.compile(r"[sS]cor[ing]*"),
        'replace_string' : 'Scr'
    },

    'SCRAMBLING_PATTERN' : {
        'pattern' : re.compile(r"[sS]cramb[a-z]*"),
        'replace_string' : 'Scram'
    },

}

# with open("stat_list.json") as stat_list:
#     all_stats = json.load(stat_list)
#     categories = all_stats['pageProps']['statOverview']['categories']

# for category in categories:
#     for sub in category['subCategories']:
#         for stat in sub['stats']:
#             if stat_id_dict.get(stat.get('statId')):
#                 continue
#             else:
#                 stat_id_dict[stat.get('statId')] = stat.get('statTitle')

# for stat_id, stat_name in stat_id_dict.items():
#     name_as_list = stat_name.split()

#     for i,chunk in enumerate(name_as_list):
          
#         chunk = chunk.replace("-","_")
#         chunk = chunk.lower()
#         name_as_list[i] = chunk

#         new_str = chunk

#         for pattern in PATTERN_DICT.keys():
#             regex = PATTERN_DICT[pattern]
#             if regex['pattern'].search(new_str):
#                 new_str = re.sub(regex['pattern'], regex['replace_string'], new_str)
        
#         name_as_list[i] = new_str


#     for string in EXTRA_WORDS:
#         name_as_list.remove(string) if string.lower() in name_as_list else None
    
#     stat_id_dict[stat_id] = '_'.join(name_as_list).lower()


# create_json_file("stat_id_dictionary.json", stat_id_dict)

with open("stat_id_dictionary.json") as stat_list:
    all_stats = json.load(stat_list)
# print(len(all_stats))
# print(len(max(list(all_stats.values()),key=len)))
# print([f"len: {len(name)} : {name}" for name in list(all_stats.values()) if len(name) > 30])

with open("drv_dist_example.json") as stat_example:
    ex = json.load(stat_example)

stat_headers = ['id', 'player', 'avg', 'total_distance', 'total_drives']

stat_types = ['SERIAL PRIMARY KEY', 'VARCHAR(255)', 'VARCHAR(255)', 'VARCHAR(255)', 'VARCHAR(255)']


url = "https://orchestrator.pgatour.com/graphql"
with open("stats_header.json") as data_completed:
    headers = json.load(data_completed)


with Database(db_type='dev') as (db, con, cur):
    select_query = """
    SELECT id, pga_id, first_name || ' ' || last_name as player_name
    from players
    """
    cur.execute(select_query)
    player_id_results = cur.fetchall()

    select_query = """
    SELECT id, pga_tournament_id
    from tournaments
    """
    cur.execute(select_query)
    tournament_id_results = cur.fetchall()


player_id_dict = {result.get("pga_id"):int(result.get("id")) for result in player_id_results }
tournament_id_dict = {result.get("pga_tournament_id"):int(result.get("id")) for result in tournament_id_results }


with Database(db_type='dev') as (db, con, cur):
    for stat in list(all_stats.keys())[:2]:
        stat_headers = ['id', 'pga_stat_id', 'pga_stat_name', 'player_id', 'thru_tournament_id']
        stat_types = ['SERIAL PRIMARY KEY', 'VARCHAR(255)', 'INT', 'VARCHAR(255)', 'INT']
        payload = f"{{\"query\":\"query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {{\\n  statDetails(\\n    tourCode: $tourCode\\n    statId: $statId\\n    year: $year\\n    eventQuery: $eventQuery\\n  ) {{\\n    tourCode\\n    year\\n    displaySeason\\n    statId\\n    statType\\n    tournamentPills {{\\n      tournamentId\\n      displayName\\n    }}\\n    yearPills {{\\n      year\\n      displaySeason\\n    }}\\n    statTitle\\n    statDescription\\n    tourAvg\\n    lastProcessed\\n    statHeaders\\n    statCategories {{\\n      category\\n      displayName\\n      subCategories {{\\n        displayName\\n        stats {{\\n          statId\\n          statTitle\\n        }}\\n      }}\\n    }}\\n    rows {{\\n      ... on StatDetailsPlayer {{\\n        __typename\\n        playerId\\n        playerName\\n        country\\n        countryFlag\\n        rank\\n        rankDiff\\n        rankChangeTendency\\n        stats {{\\n          statName\\n          statValue\\n          color\\n        }}\\n      }}\\n      ... on StatDetailTourAvg {{\\n        __typename\\n        displayName\\n        value\\n      }}\\n    }}\\n    sponsorLogo\\n  }}\\n}}\",\"operationName\":\"StatDetails\",\"variables\":{{\"tourCode\":\"R\",\"statId\":\"{stat}\",\"year\":2023,\"eventQuery\":{{\"queryType\":\"THROUGH_EVENT\",\"tournamentId\":\"R2023007\"}}}}}}"
        time.sleep(3)
        response = requests.request("POST", url, data=payload, headers=headers)
        stats = response.json()

        for stat_header in stats['data']['statDetails']['statHeaders']:
            stat_headers.append(stat_header)
            stat_types.append("VARCHAR(255)")

        # print(stat_headers,"\n",stat_types)

        table_name = all_stats.get(stat)

        db.create_table(table_name, stat_headers, stat_types)