import requests
import time
import json
from database import Database
import queries
import re
from utils import create_json_file, get_column_names
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation, UndefinedTable

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

with open("sg_tot_example.json") as stat_example:
    ex = json.load(stat_example)


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

    thru_tourn_select = """
    select
    id
    ,pga_tournament_id
    ,tournament_end_date
    
    from tournaments
    
    where tournament_end_date IS NOT NULL
    AND season_year = '2022 - 2023'
    AND lower(tournament_name) NOT LIKE 'corales%'
    AND lower(tournament_name) NOT LIKE 'puerto rico%'
    AND lower(tournament_name) NOT LIKE 'butterfield%'
    order by tournament_end_date desc  
    """
    cur.execute(thru_tourn_select)
    thru_tourn_results = cur.fetchall()

player_id_dict = {result.get("pga_id"):int(result.get("id")) for result in player_id_results }
tournament_id_dict = {result.get("pga_tournament_id"):int(result.get("id")) for result in tournament_id_results }
thru_tourn_list = [result.get("pga_tournament_id") for result in thru_tourn_results]

with Database(db_type='dev') as (db, con, cur):
    for tournament in thru_tourn_list:
        print(tournament)
        for stat in list(all_stats.keys())[:10]:        
            print(all_stats.get(stat))
            table_name = all_stats.get(stat)

            time.sleep(7)
            payload = f"{{\"query\":\"query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {{\\n  statDetails(\\n    tourCode: $tourCode\\n    statId: $statId\\n    year: $year\\n    eventQuery: $eventQuery\\n  ) {{\\n    tourCode\\n    year\\n    displaySeason\\n    statId\\n    statType\\n    tournamentPills {{\\n      tournamentId\\n      displayName\\n    }}\\n    yearPills {{\\n      year\\n      displaySeason\\n    }}\\n    statTitle\\n    statDescription\\n    tourAvg\\n    lastProcessed\\n    statHeaders\\n    statCategories {{\\n      category\\n      displayName\\n      subCategories {{\\n        displayName\\n        stats {{\\n          statId\\n          statTitle\\n        }}\\n      }}\\n    }}\\n    rows {{\\n      ... on StatDetailsPlayer {{\\n        __typename\\n        playerId\\n        playerName\\n        country\\n        countryFlag\\n        rank\\n        rankDiff\\n        rankChangeTendency\\n        stats {{\\n          statName\\n          statValue\\n          color\\n        }}\\n      }}\\n      ... on StatDetailTourAvg {{\\n        __typename\\n        displayName\\n        value\\n      }}\\n    }}\\n    sponsorLogo\\n  }}\\n}}\",\"operationName\":\"StatDetails\",\"variables\":{{\"tourCode\":\"R\",\"statId\":\"{stat}\",\"year\":2023,\"eventQuery\":{{\"queryType\":\"THROUGH_EVENT\",\"tournamentId\":\"{tournament}\"}}}}}}"
            response = requests.request("POST", url, data=payload, headers=headers)
            stats = response.json()

            try:
                query = sql.SQL("""SELECT 1 FROM {}""").format(
                sql.Identifier(table_name))
                cur.execute(query)

            except UndefinedTable: 
                print("table undefined")
                con.rollback()        
                stat_headers = ['id', 'pga_stat_id', 'pga_stat_name', 'player_id', 'thru_tournament_id', 'rank']
                stat_types = ['SERIAL PRIMARY KEY', 'VARCHAR(255)', 'VARCHAR(255)', 'INT', 'INT', 'INT']

                for stat_header in stats['data']['statDetails']['statHeaders']:
                    if stat_header.lower() in ('avg', 'average'):
                        stat_header = 'avg_val'
                    stat_headers.append(stat_header)
                    stat_types.append("VARCHAR(255)")

                db.create_table(table_name, stat_headers, stat_types, ['player_id', 'pga_stat_id', 'thru_tournament_id'])
                

            finally:
                
                cols = get_column_names('public', table_name, cur)[1:]
                print(cols)
                # cols = stat_headers[1:]
                vals = []

                for row in stats['data']['statDetails']['rows']:
                    if row['__typename'] != 'StatDetailsPlayer':
                        continue
                    else:
                        pga_stat_id = stat
                        pga_stat_name = stats['data']['statDetails']['statTitle']
                        try:
                            player_id = player_id_dict.get(row['playerId'])
                        except KeyError:
                            player_id = None
                        
                        thru_tournament_id = tournament_id_dict.get(tournament)
                        rank = row['rank']

                        row_vals = [pga_stat_id, pga_stat_name, player_id, thru_tournament_id, rank]

                        for val in row['stats']:
                            row_vals.append(val['statValue'])

                        vals.append(tuple(row_vals))
        
                db.bulk_insert(table_name, cols, vals)