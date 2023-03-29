import json


def create_json_file(filename, dictionary):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)


def name_clean(name_string):
    name_as_list = [*name_string]
    name = ''
    for i,char in enumerate(name_as_list[::-1]):
        if i == 0 and char == "." or char == ",":
            continue
        else:
            if char == ' ':
                name += "-"
            else:
                name += char
    return name[::-1]

COUNTRY_NAME_MAP = {
    'Korea;': 'Korea',
    'Venezuala': 'Venezuela'
}

COUNTRIES_FOR_OWGR = [
    'Africa',
    'Argentina',
    'Australia',
    'Austria',
    'Bangladesh',
    'Belgium',
    'Brazil',
    'Canada',
    'Chile',
    'China',
    'Colombia',
    'Denmark',
    'England',
    'Fiji',
    'Finland',
    'France',
    'Germany',
    'Greece',
    'Holland',
    'India',
    'Ireland',
    'Italy',
    'Japan',
    'Korea',
    'Korea;',
    'Malaysia',
    'Mexico',
    'Netherlands',
    'Norway',
    'Paraguay',
    'Philippines',
    'Poland',
    'Portugal',
    'Republic',
    'Rico',
    'Scotland',
    'Singapore',
    'Slovakia',
    'Spain',
    'States',
    'Sweden',
    'Switzerland',
    'Taipei',
    'Thailand',
    'Venezuela',
    'Venezuala',
    'Wales',
    'Zealand',
    'Zimbabwe',
    'ARG',
    'AUS',
    'AUT',
    'BEL',
    'CAN',
    'CHI',
    'CHN',
    'COL',
    'DEN',
    'ENG',
    'ESP',
    'FIJ',
    'FIN',
    'FRA',
    'GER',
    'GRE',
    'IND',
    'IRL',
    'ITA',
    'JPN',
    'KOR',
    'MAS',
    'MEX',
    'NED',
    'NIR',
    'NOR',
    'NZL',
    'PAR',
    'PHI',
    'POR',
    'RSA',
    'SCO',
    'SVK',
    'SWE',
    'THA',
    'TPE',
    'USA',
    'VEN',
    'WAL',
    'ZIM',
    '(Chinese',
    '(Chines',
]

COUNTRY_PREFIX_FOR_OWGR = [
    'United',
    'N',
    'South',
    'New',
    'Chinese',
    'Czech',
    'Korea;',
    'Northern',
    'Puerto',
    'Taiwan',
]

COUNTRY_CONCAT_WORDS_FOR_OWGR = [
    'of',
    'Taipei)'
]