import json

def get_column_names(schema, table_name, cur):
    col_query = """
    SELECT * 
    FROM  information_schema.columns 
    WHERE table_schema = %s 
    and table_name = %s
    order by
    ordinal_position
    """

    cur.execute(col_query, (schema, table_name))
    col_results = cur.fetchall()
 
    return [result.get("column_name") for result in col_results]



def create_json_file(filename, dictionary):
    with open(filename, 'w', encoding='utf-8') as file:
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
    'PUE',
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


PLAYER_NAME_CLEANUP = {
    'Cameron Davis': 'Cam Davis',
    'Marty Dou Zecheng': 'Zecheng Dou',
    'Marty Dou Ze-cheng': 'Zecheng Dou',
    'Dou Ze-cheng': 'Zecheng Dou',
    'Nicolas Echavarria': 'Nico Echavarria',
    'Fabian Gomez': 'Fabián Gómez',
    'William Gordon': 'Will Gordon',
    'Paul Haley-II': 'Paul Haley II',
    'Sunghoon Kang': 'Sung Kang',
    'Seonghyeon Kim': 'S.H. Kim',
    'Kyoung-Hoon Lee': 'K.H. Lee',
    'Kyounghoon Lee': 'K.H. Lee',
    'KH Lee': 'K.H. Lee',
    'Seungyul Noh': 'S.Y. Noh',
    'Augusto Nunez': 'Augusto Núñez',
    'Ted Potter Jr': 'Ted Potter, Jr.',
    'Ted Potter-jr': 'Ted Potter, Jr.',
    'Robby Shelton IV': 'Robby Shelton',
    'Samuel Stevens': 'Sam Stevens',
    'Benjamin Taylor': 'Ben Taylor',
    'Vincent Whaley': 'Vince Whaley',
    'Chun-an Yu': 'Kevin Yu',
    'Yechun Carl Yuan': 'Carl Yuan',
    'Yuan Carl Yechun': 'Carl Yuan',
    'J.J Spaun': 'J.J. Spaun',
    'J.J Henry': 'J.J. Henry',
    'J.B Holmes': 'J.B. Holmes',
    'C.T Pan': 'C.T. Pan',
    'D.A Points': 'D.A. Points',
    'J.T Poston': 'J.T. Poston',
    'JT Poston' : 'J.T. Poston',
    'D.J Trahan': 'D.J. Trahan',
    'Minwoo Lee': 'Min Woo Lee',
    'Benjamin Griffin(May1996)':'Ben Griffin',
    'Davis Love-III' : 'Davis Love III',
    'Siwoo Kim': 'Si Woo Kim',
    'Bryan': 'Wesley Bryan',
    'Matthew Every': 'Matt Every',
    'Hideki Matsuyama(Am)': 'Hideki Matsuyama',
    'Matthew Fitzpatrick': 'Matt Fitzpatrick',
    'Guillermo Mito Pereira': 'Mito Pereira',
    'Tyler Duncan(Jul1989)': 'Tyler Duncan',

}

PLAYER_ID_DICT = {
    "Anders Albertson": {"player_id": 1, "pga_id": "49303"},
    "Tyson Alexander": {"player_id": 2, "pga_id": "33408"},
    "Byeong Hun An": {"player_id": 3, "pga_id": "33948"},
    "Ryan Armour": {"player_id": 4, "pga_id": "19803"},
    "Aaron Baddeley": {"player_id": 5, "pga_id": "22371"},
    "Sangmoon Bae": {"player_id": 6, "pga_id": "28259"},
    "Briny Baird": {"player_id": 7, "pga_id": "20498"},
    "Erik Barnes": {"player_id": 8, "pga_id": "34374"},
    "Ricky Barnes": {"player_id": 9, "pga_id": "24846"},
    "Daniel Berger": {"player_id": 10, "pga_id": "40026"},
    "Christiaan Bezuidenhout": {"player_id": 11, "pga_id": "45522"},
    "Zac Blair": {"player_id": 12, "pga_id": "40058"},
    "Jonas Blixt": {"player_id": 13, "pga_id": "27895"},
    "Keegan Bradley": {"player_id": 14, "pga_id": "33141"},
    "Joseph Bramlett": {"player_id": 15, "pga_id": "34255"},
    "Ryan Brehm": {"player_id": 16, "pga_id": "28420"},
    "Scott Brown": {"player_id": 17, "pga_id": "29479"},
    "Wesley Bryan": {"player_id": 18, "pga_id": "48084"},
    "Hayden Buckley": {"player_id": 19, "pga_id": "55708"},
    "Bronson Burgoon": {"player_id": 20, "pga_id": "29268"},
    "Sam Burns": {"player_id": 21, "pga_id": "47504"},
    "Jonathan Byrd": {"player_id": 22, "pga_id": "24925"},
    "Patrick Cantlay": {"player_id": 23, "pga_id": "35450"},
    "Bud Cauley": {"player_id": 24, "pga_id": "34021"},
    "Greg Chalmers": {"player_id": 25, "pga_id": "20593"},
    "Cameron Champ": {"player_id": 26, "pga_id": "52372"},
    "Kevin Chappell": {"player_id": 27, "pga_id": "32366"},
    "Stewart Cink": {"player_id": 28, "pga_id": "20229"},
    "Tim Clark": {"player_id": 29, "pga_id": "23135"},
    "Wyndham Clark": {"player_id": 30, "pga_id": "51766"},
    "Eric Cole": {"player_id": 31, "pga_id": "47591"},
    "Chad Collins": {"player_id": 32, "pga_id": "25720"},
    "Trevor Cone": {"player_id": 33, "pga_id": "49453"},
    "Corey Conners": {"player_id": 34, "pga_id": "39997"},
    "Austin Cook": {"player_id": 35, "pga_id": "46435"},
    "Vince Covello": {"player_id": 36, "pga_id": "32982"},
    "Ben Crane": {"player_id": 37, "pga_id": "23541"},
    "MJ Daffue": {"player_id": 38, "pga_id": "39067"},
    "Joel Dahmen": {"player_id": 39, "pga_id": "34076"},
    "Brian Davis": {"player_id": 40, "pga_id": "21753"},
    "Cam Davis": {"player_id": 41, "pga_id": "45157"},
    "Jason Day": {"player_id": 42, "pga_id": "28089"},
    "Thomas Detry": {"player_id": 43, "pga_id": "33653"},
    "Luke Donald": {"player_id": 44, "pga_id": "23983"},
    "Zecheng Dou": {"player_id": 45, "pga_id": "37338"},
    "Jason Dufner": {"player_id": 46, "pga_id": "25686"},
    "Tyler Duncan": {"player_id": 47, "pga_id": "45609"},
    "Nico Echavarria": {"player_id": 48, "pga_id": "51349"},
    "Austin Eckroat": {"player_id": 49, "pga_id": "57362"},
    "Harrison Endycott": {"player_id": 50, "pga_id": "47079"},
    "Harris English": {"player_id": 51, "pga_id": "34099"},
    "Matt Every": {"player_id": 52, "pga_id": "28307"},
    "Tony Finau": {"player_id": 53, "pga_id": "29725"},
    "Matt Fitzpatrick": {"player_id": 54, "pga_id": "40098"},
    "Tommy Fleetwood": {"player_id": 55, "pga_id": "30911"},
    "Rickie Fowler": {"player_id": 56, "pga_id": "32102"},
    "Dylan Frittelli": {"player_id": 57, "pga_id": "29970"},
    "Jim Furyk": {"player_id": 58, "pga_id": "10809"},
    "Brice Garnett": {"player_id": 59, "pga_id": "29535"},
    "Robert Garrigus": {"player_id": 60, "pga_id": "24358"},
    "Doug Ghim": {"player_id": 61, "pga_id": "52375"},
    "Michael Gligic": {"player_id": 62, "pga_id": "32662"},
    "Lucas Glover": {"player_id": 63, "pga_id": "25900"},
    "Fabián Gómez": {"player_id": 64, "pga_id": "28679"},
    "Will Gordon": {"player_id": 65, "pga_id": "56762"},
    "Tano Goya": {"player_id": 66, "pga_id": "31577"},
    "Brent Grant": {"player_id": 67, "pga_id": "51414"},
    "Ben Griffin": {"player_id": 68, "pga_id": "54591"},
    "Lanto Griffin": {"player_id": 69, "pga_id": "35310"},
    "Emiliano Grillo": {"player_id": 70, "pga_id": "31646"},
    "Bill Haas": {"player_id": 71, "pga_id": "24924"},
    "Chesson Hadley": {"player_id": 72, "pga_id": "34563"},
    "Adam Hadwin": {"player_id": 73, "pga_id": "33399"},
    "James Hahn": {"player_id": 74, "pga_id": "32448"},
    "Paul Haley II": {"player_id": 75, "pga_id": "35901"},
    "Harry Hall": {"player_id": 76, "pga_id": "57975"},
    "Nick Hardy": {"player_id": 77, "pga_id": "47988"},
    "Brian Harman": {"player_id": 78, "pga_id": "27644"},
    "Scott Harrington": {"player_id": 79, "pga_id": "27554"},
    "Tyrrell Hatton": {"player_id": 80, "pga_id": "34363"},
    "David Hearn": {"player_id": 81, "pga_id": "26758"},
    "Russell Henley": {"player_id": 82, "pga_id": "34098"},
    "J.J. Henry": {"player_id": 83, "pga_id": "23353"},
    "Lucas Herbert": {"player_id": 84, "pga_id": "39058"},
    "Jim Herman": {"player_id": 85, "pga_id": "31557"},
    "Kramer Hickok": {"player_id": 86, "pga_id": "49298"},
    "Garrick Higgo": {"player_id": 87, "pga_id": "54421"},
    "Harry Higgs": {"player_id": 88, "pga_id": "33597"},
    "Lee Hodges": {"player_id": 89, "pga_id": "54628"},
    "Charley Hoffman": {"player_id": 90, "pga_id": "12716"},
    "Tom Hoge": {"player_id": 91, "pga_id": "35532"},
    "J.B. Holmes": {"player_id": 92, "pga_id": "27141"},
    "Max Homa": {"player_id": 93, "pga_id": "39977"},
    "Billy Horschel": {"player_id": 94, "pga_id": "29420"},
    "Beau Hossler": {"player_id": 95, "pga_id": "35461"},
    "Viktor Hovland": {"player_id": 96, "pga_id": "46717"},
    "Mark Hubbard": {"player_id": 97, "pga_id": "36801"},
    "Mackenzie Hughes": {"player_id": 98, "pga_id": "35506"},
    "John Huh": {"player_id": 99, "pga_id": "34174"},
    "Sungjae Im": {"player_id": 100, "pga_id": "39971"},
    "Stephan Jaeger": {"player_id": 101, "pga_id": "36799"},
    "Richard Johnson": {"player_id": 102, "pga_id": "26420"},
    "Zach Johnson": {"player_id": 103, "pga_id": "24024"},
    "Sung Kang": {"player_id": 104, "pga_id": "27974"},
    "Michael Kim": {"player_id": 105, "pga_id": "39975"},
    "S.H. Kim": {"player_id": 106, "pga_id": "50188"},
    "Si Woo Kim": {"player_id": 107, "pga_id": "37455"},
    "Tom Kim": {"player_id": 108, "pga_id": "55182"},
    "Chris Kirk": {"player_id": 109, "pga_id": "30926"},
    "Kevin Kisner": {"player_id": 110, "pga_id": "29478"},
    "Kurt Kitayama": {"player_id": 111, "pga_id": "48117"},
    "Patton Kizzire": {"player_id": 112, "pga_id": "32757"},
    "Philip Knowles": {"player_id": 113, "pga_id": "54813"},
    "Russell Knox": {"player_id": 114, "pga_id": "33122"},
    "Satoshi Kodaira": {"player_id": 115, "pga_id": "32816"},
    "Kelly Kraft": {"player_id": 116, "pga_id": "35879"},
    "Matt Kuchar": {"player_id": 117, "pga_id": "23108"},
    "Martin Laird": {"player_id": 118, "pga_id": "27936"},
    "Andrew Landry": {"player_id": 119, "pga_id": "33410"},
    "Nate Lashley": {"player_id": 120, "pga_id": "28775"},
    "Hank Lebioda": {"player_id": 121, "pga_id": "49766"},
    "K.H. Lee": {"player_id": 122, "pga_id": "32791"},
    "Nicholas Lindheim": {"player_id": 123, "pga_id": "37278"},
    "David Lingmerth": {"player_id": 124, "pga_id": "34409"},
    "David Lipsky": {"player_id": 125, "pga_id": "36326"},
    "Luke List": {"player_id": 126, "pga_id": "27129"},
    "Adam Long": {"player_id": 127, "pga_id": "35449"},
    "Davis Love III": {"player_id": 128, "pga_id": "01706"},
    "Justin Lower": {"player_id": 129, "pga_id": "40162"},
    "Shane Lowry": {"player_id": 130, "pga_id": "33204"},
    "Peter Malnati": {"player_id": 131, "pga_id": "34466"},
    "Ben Martin": {"player_id": 132, "pga_id": "33413"},
    "Hideki Matsuyama": {"player_id": 133, "pga_id": "32839"},
    "Brandon Matthews": {"player_id": 134, "pga_id": "51491"},
    "Denny McCarthy": {"player_id": 135, "pga_id": "47993"},
    "Tyler McCumber": {"player_id": 136, "pga_id": "40042"},
    "William McGirt": {"player_id": 137, "pga_id": "31202"},
    "Max McGreevy": {"player_id": 138, "pga_id": "51950"},
    "Rory McIlroy": {"player_id": 139, "pga_id": "28237"},
    "Maverick McNealy": {"player_id": 140, "pga_id": "46442"},
    "John Merrick": {"player_id": 141, "pga_id": "27933"},
    "Troy Merritt": {"player_id": 142, "pga_id": "32640"},
    "Keith Mitchell": {"player_id": 143, "pga_id": "39546"},
    "Francesco Molinari": {"player_id": 144, "pga_id": "25198"},
    "Taylor Montgomery": {"player_id": 145, "pga_id": "55789"},
    "Ryan Moore": {"player_id": 146, "pga_id": "26596"},
    "Taylor Moore": {"player_id": 147, "pga_id": "49947"},
    "Collin Morikawa": {"player_id": 148, "pga_id": "50525"},
    "Trey Mullinax": {"player_id": 149, "pga_id": "46601"},
    "Grayson Murray": {"player_id": 150, "pga_id": "34213"},
    "Matthew NeSmith": {"player_id": 151, "pga_id": "36871"},
    "S.Y. Noh": {"player_id": 152, "pga_id": "29289"},
    "Alex Noren": {"player_id": 153, "pga_id": "27349"},
    "Henrik Norlander": {"player_id": 154, "pga_id": "30163"},
    "Vincent Norrman": {"player_id": 155, "pga_id": "51070"},
    "Andrew Novak": {"player_id": 156, "pga_id": "51997"},
    "Augusto Núñez": {"player_id": 157, "pga_id": "36724"},
    "Sean O'Hair": {"player_id": 158, "pga_id": "24140"},
    "Ryan Palmer": {"player_id": 159, "pga_id": "23320"},
    "C.T. Pan": {"player_id": 160, "pga_id": "29908"},
    "Taylor Pendrith": {"player_id": 161, "pga_id": "40250"},
    "Cameron Percy": {"player_id": 162, "pga_id": "22056"},
    "Scott Piercy": {"player_id": 163, "pga_id": "25818"},
    "D.A. Points": {"player_id": 164, "pga_id": "25240"},
    "J.T. Poston": {"player_id": 165, "pga_id": "49771"},
    "Ted Potter, Jr.": {"player_id": 166, "pga_id": "27556"},
    "Seamus Power": {"player_id": 167, "pga_id": "28252"},
    "Andrew Putnam": {"player_id": 168, "pga_id": "34256"},
    "Jon Rahm": {"player_id": 169, "pga_id": "46970"},
    "Aaron Rai": {"player_id": 170, "pga_id": "46414"},
    "Chad Ramey": {"player_id": 171, "pga_id": "47983"},
    "Chez Reavie": {"player_id": 172, "pga_id": "26476"},
    "Doc Redman": {"player_id": 173, "pga_id": "53165"},
    "Davis Riley": {"player_id": 174, "pga_id": "47995"},
    "Patrick Rodgers": {"player_id": 175, "pga_id": "36699"},
    "Justin Rose": {"player_id": 176, "pga_id": "22405"},
    "Kevin Roy": {"player_id": 177, "pga_id": "39335"},
    "Sam Ryder": {"player_id": 178, "pga_id": "37275"},
    "Rory Sabbatini": {"player_id": 179, "pga_id": "23621"},
    "Xander Schauffele": {"player_id": 180, "pga_id": "48081"},
    "Scottie Scheffler": {"player_id": 181, "pga_id": "46046"},
    "Adam Schenk": {"player_id": 182, "pga_id": "47347"},
    "Matti Schmid": {"player_id": 183, "pga_id": "48867"},
    "Matthias Schwab": {"player_id": 184, "pga_id": "34610"},
    "Adam Scott": {"player_id": 185, "pga_id": "24502"},
    "Robby Shelton": {"player_id": 186, "pga_id": "46441"},
    "Greyson Sigg": {"player_id": 187, "pga_id": "51890"},
    "Webb Simpson": {"player_id": 188, "pga_id": "29221"},
    "Vijay Singh": {"player_id": 189, "pga_id": "06567"},
    "Alex Smalley": {"player_id": 190, "pga_id": "46340"},
    "Austin Smotherman": {"player_id": 191, "pga_id": "50095"},
    "Brandt Snedeker": {"player_id": 192, "pga_id": "27649"},
    "J.J. Spaun": {"player_id": 193, "pga_id": "39324"},
    "Jordan Spieth": {"player_id": 194, "pga_id": "34046"},
    "Kevin Stadler": {"player_id": 195, "pga_id": "26679"},
    "Scott Stallings": {"player_id": 196, "pga_id": "30692"},
    "Kyle Stanley": {"player_id": 197, "pga_id": "30110"},
    "Sam Stevens": {"player_id": 198, "pga_id": "55893"},
    "Sepp Straka": {"player_id": 199, "pga_id": "49960"},
    "Robert Streb": {"player_id": 200, "pga_id": "34431"},
    "Kevin Streelman": {"player_id": 201, "pga_id": "27214"},
    "Chris Stroud": {"player_id": 202, "pga_id": "27963"},
    "Brian Stuard": {"player_id": 203, "pga_id": "31560"},
    "Justin Suh": {"player_id": 204, "pga_id": "50493"},
    "Adam Svensson": {"player_id": 205, "pga_id": "40115"},
    "Callum Tarren": {"player_id": 206, "pga_id": "48699"},
    "Ben Taylor": {"player_id": 207, "pga_id": "48119"},
    "Nick Taylor": {"player_id": 208, "pga_id": "25493"},
    "Vaughn Taylor": {"player_id": 209, "pga_id": "23325"},
    "Sahith Theegala": {"player_id": 210, "pga_id": "51634"},
    "Justin Thomas": {"player_id": 211, "pga_id": "33448"},
    "Davis Thompson": {"player_id": 212, "pga_id": "58168"},
    "Michael Thompson": {"player_id": 213, "pga_id": "32150"},
    "Brendon Todd": {"player_id": 214, "pga_id": "30927"},
    "D.J. Trahan": {"player_id": 215, "pga_id": "23788"},
    "Martin Trainer": {"player_id": 216, "pga_id": "35617"},
    "Kevin Tway": {"player_id": 217, "pga_id": "32333"},
    "Bo Van Pelt": {"player_id": 218, "pga_id": "23623"},
    "Erik van Rooyen": {"player_id": 219, "pga_id": "40006"},
    "Jhonattan Vegas": {"player_id": 220, "pga_id": "27064"},
    "Camilo Villegas": {"player_id": 221, "pga_id": "27770"},
    "Jimmy Walker": {"player_id": 222, "pga_id": "25632"},
    "Matt Wallace": {"player_id": 223, "pga_id": "48887"},
    "Nick Watney": {"player_id": 224, "pga_id": "27095"},
    "Trevor Werbylo": {"player_id": 225, "pga_id": "58967"},
    "Richy Werenski": {"player_id": 226, "pga_id": "47128"},
    "Kyle Westmoreland": {"player_id": 227, "pga_id": "52411"},
    "Vince Whaley": {"player_id": 228, "pga_id": "51894"},
    "Tim Wilkinson": {"player_id": 229, "pga_id": "25349"},
    "Danny Willett": {"player_id": 230, "pga_id": "32139"},
    "Aaron Wise": {"player_id": 231, "pga_id": "49964"},
    "Gary Woodland": {"player_id": 232, "pga_id": "31323"},
    "Tiger Woods": {"player_id": 233, "pga_id": "08793"},
    "Brandon Wu": {"player_id": 234, "pga_id": "52374"},
    "Dylan Wu": {"player_id": 235, "pga_id": "54783"},
    "Cameron Young": {"player_id": 236, "pga_id": "57366"},
    "Carson Young": {"player_id": 237, "pga_id": "52513"},
    "Kevin Yu": {"player_id": 238, "pga_id": "45242"},
    "Carl Yuan": {"player_id": 239, "pga_id": "55454"},
    "Will Zalatoris": {"player_id": 240, "pga_id": "47483"},
    "Akshay Bhatia": {"player_id": 241, "pga_id": "56630"},
}