import json
import re
from utils import create_json_file, get_column_names

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
        chunk = chunk.lower()
        name_as_list[i] = chunk

        new_str = chunk

        for pattern in PATTERN_DICT.keys():
            regex = PATTERN_DICT[pattern]
            if regex['pattern'].search(new_str):
                new_str = re.sub(regex['pattern'], regex['replace_string'], new_str)
        
        name_as_list[i] = new_str


    for string in EXTRA_WORDS:
        name_as_list.remove(string) if string.lower() in name_as_list else None
    
    stat_id_dict[stat_id] = '_'.join(name_as_list).lower()

# create_json_file("stat_id_dictionary.json", stat_id_dict)