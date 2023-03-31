import requests
import time
import json
from database import Database
import queries
import re
from utils import create_json_file

# stat_id_dict = {}
# # NON_ALPHA_PATTERN = re.compile(r'\W+')
# NON_ALPHA_PATTERN = re.compile(r"[:\.,\s,\(,\)']+")

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
#         name_as_list[i] = chunk
               
#         file_match = NON_ALPHA_PATTERN.search(chunk)
#         if file_match:
#             new_str = re.sub(NON_ALPHA_PATTERN,"",chunk)
#             name_as_list[i] = new_str
    
#     name_as_list.remove("_") if "_" in name_as_list else None
#     name_as_list.remove("®") if "®" in name_as_list else None
    
#     stat_id_dict[stat_id] = '_'.join(name_as_list)


# create_json_file("stat_id_dictionary.json", stat_id_dict)

with open("stat_id_dictionary.json") as stat_list:
    all_stats = json.load(stat_list)
print(len(all_stats))
print(len(max(list(all_stats.values()),key=len)))
print([f"len: {len(name)} : {name}" for name in list(all_stats.values()) if len(name) > 30])




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




