import requests
import time
import json
from database import Database
import queries
import re
from utils import create_json_file

stat_id_dict = {}

EXTRA_WORDS = ('by', 'measured', '_', '®', 'from', 'the')

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

}

with open("stat_list.json") as stat_list:
    all_stats = json.load(stat_list)
    categories = all_stats['pageProps']['statOverview']['categories']

for category in categories:
    for sub in category['subCategories']:
        for stat in sub['stats']:
            if stat_id_dict.get(stat.get('statId')):
                continue
            else:
                stat_id_dict[stat.get('statId')] = stat.get('statTitle')

for stat_id, stat_name in stat_id_dict.items():
    name_as_list = stat_name.split()

    for i,chunk in enumerate(name_as_list):
          
        chunk = chunk.replace("-","_")
        name_as_list[i] = chunk

        new_str = chunk

        for pattern in PATTERN_DICT.keys():
            if PATTERN_DICT[pattern]['pattern'].search(new_str):
                new_str = re.sub(PATTERN_DICT[pattern]['pattern'], PATTERN_DICT[pattern]['replace_string'], new_str)
        # if NON_ALPHA_PATTERN.search(new_str):
        #     new_str = re.sub(NON_ALPHA_PATTERN,"",new_str)

        # if APPROACH_PATTERN.search(new_str):
        #     new_str = re.sub(APPROACH_PATTERN,"App",new_str)

        # if PERCENTAGE_PATTERN.search(new_str):
        #     new_str = re.sub(PERCENTAGE_PATTERN,"Pct",new_str)

        # if DRIVING_PATTERN.search(new_str):
        #     new_str = re.sub(DRIVING_PATTERN,"Drv",new_str)
        
        # if YARDAGE_PATTERN.search(new_str):
        #     new_str = re.sub(YARDAGE_PATTERN,"Yrd",new_str)
        
        # if FAIRWAY_PATTERN.search(new_str):
        #     new_str = re.sub(FAIRWAY_PATTERN,"Fwy",new_str)
        
        # if ROUGH_PATTERN.search(new_str):
        #     new_str = re.sub(ROUGH_PATTERN,"Rgh",new_str)
        
        # if BIRDIE_PATTERN.search(new_str):
        #     new_str = re.sub(BIRDIE_PATTERN,"Brd",new_str)

        # if BOGEY_PATTERN.search(new_str):
        #     new_str = re.sub(BOGEY_PATTERN,"Bgy",new_str)

        # if PROXIMITY_PATTERN.search(new_str):
        #     new_str = re.sub(PROXIMITY_PATTERN,"Prox",new_str)

        # if AVERAGE_PATTERN.search(new_str):
        #     new_str = re.sub(AVERAGE_PATTERN,"Avg",new_str)
        
        # if EFFICIENCY_PATTERN.search(new_str):
        #     new_str = re.sub(EFFICIENCY_PATTERN,"Eff",new_str) 

        
        name_as_list[i] = new_str


    for string in EXTRA_WORDS:
        name_as_list.remove(string) if string in name_as_list else None
    
    stat_id_dict[stat_id] = '_'.join(name_as_list).lower()


create_json_file("stat_id_dictionary.json", stat_id_dict)

# with open("stat_id_dictionary.json") as stat_list:
#     all_stats = json.load(stat_list)
# print(len(all_stats))
# print(len(max(list(all_stats.values()),key=len)))
# print([f"len: {len(name)} : {name}" for name in list(all_stats.values()) if len(name) > 30])




# url = "https://orchestrator.pgatour.com/graphql"

# with open("schedule_header.json") as data_completed:
#     headers = json.load(data_completed)




# with Database(db_type='dev') as (con, cur):
#     select_tournament_ids = """
#     SELECT
#     id,
#     pga_tournament_id
#     FROM tournaments
#     /* WHERE id > 80 */
#     """

#     cur.execute(select_tournament_ids)
#     results = cur.fetchall()

#     for result in results:
#         print(result)
#         insert_course_data = """
#         INSERT INTO courses (
#             course_name,
#             course_id_pga,
#             city,
#             state,
#             country
#         )
        
#         VALUES
#         (%s, %s, %s, %s, %s)
        
#         """
#         payload_for_course_id = f"{{\"query\":\"query Tournaments($ids: [ID!]) {{\\n  tournaments(ids: $ids) {{\\n    id\\n    tournamentName\\n    tournamentLogo\\n    tournamentLocation\\n    tournamentStatus\\n    roundStatusDisplay\\n    roundDisplay\\n    roundStatus\\n    roundStatusColor\\n    currentRound\\n    timezone\\n    pdfUrl\\n    seasonYear\\n    displayDate\\n    country\\n    state\\n    city\\n    scoredLevel\\n    events {{\\n      id\\n      eventName\\n      leaderboardId\\n    }}\\n    courses {{\\n      id\\n      courseName\\n      courseCode\\n      hostCourse\\n      scoringLevel\\n    }}\\n    weather {{\\n      logo\\n      logoDark\\n      logoAccessibility\\n      tempF\\n      tempC\\n      condition\\n      windDirection\\n      windSpeedMPH\\n      windSpeedKPH\\n      precipitation\\n      humidity\\n    }}\\n    ticketsURL\\n    tournamentSiteURL\\n    formatType\\n    features\\n  }}\\n}}\",\"operationName\":\"Tournaments\",\"variables\":{{\"ids\":\"{result.get('pga_tournament_id')}\"}}}}" 
#         time.sleep(7)
#         response = requests.request("POST", url, data=payload_for_course_id, headers=headers)
        
        
#         all_data = response.json()

#         try:
#             tournament_data = all_data['data']['tournaments'][0]
#         except TypeError:
#             tournaments_without_course.append(result.get('pga_tournament_id'))
#         else:
            
#             for course in tournament_data['courses']:
#                 if course['id'] in courses_added:
#                     continue
#                 else:
#                     course_name = course['courseName']
#                     course_id_pga = course['id']
#                     city = tournament_data['city']
#                     state = tournament_data['state']
#                     country = tournament_data['country']

#                     data_completed = (
#                         course_name, 
#                         course_id_pga,
#                         city,
#                         state,
#                         country
#                         )

#                     cur.execute(insert_course_data, data_completed)
#                     con.commit()
#                     courses_added.append(course_id_pga)




