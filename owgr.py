import os
import re
from PyPDF2 import PdfReader
import pandas as pd
from utils import COUNTRIES_FOR_OWGR, COUNTRY_PREFIX_FOR_OWGR, COUNTRY_NAME_MAP, \
    COUNTRY_CONCAT_WORDS_FOR_OWGR, PLAYER_NAME_CLEANUP, PLAYER_ID_DICT
import datetime
from database import Database
from queries import OWGR_INSERT_QUERY, OWGR_INSERT_QUERY_BY_COPY


PDF_FILEPATH = 'owgr_pdfs/'
CSV_FILEPATH = 'owgr_csvs/'

ROW_START_PATTERN = re.compile(r'^\([0-9]+\)$')
AVG_POINT_PATTERN = re.compile(r'^[0-9]+\.[0-9]+$')
PDF_FILENAME_PATTERN = re.compile(r'^owgr(?P<week>[0-9]{2})f(?P<year>[0-9]{4}).pdf$')

# end_prev_year_index = None

# *********** FUNCTION DEFINITIONS **************
# ***********************************************

def read_pdf(pdf_file):
    raw_text = []
    with open(pdf_file, "rb") as file:
        pdf = PdfReader(file)
        for page in pdf.pages:
            raw_text.append(page.extract_text().split())
   
    return raw_text

def rename_owgr_files(folder='owgr_pdfs',):
    old_format_pattern = re.compile(r'^(?P<year>[0-9]{4})_(?P<week>[0-9]{2})OWGR(?P<pdf_ext>\.pdf$)')
    for filename in os.listdir(folder):
        file_match = old_format_pattern.search(filename)
        if file_match:
            dst = f"owgr{file_match.group('week')}f{file_match.group('year')}.pdf"
            src = f"{folder}/{filename}"
            dst = f"{folder}/{dst}"
            os.rename(src, dst)

def clean_week_strings(char: str):
    char = char.replace("(","")
    char = char.replace(")","")
    char = char.replace("<","")
    char = char.replace(">","")
    return char

def clean_full_name(end_prev_yr_index: int, stop_index):
    full_name_list = []
    for j in range(end_prev_yr_index, stop_index):
        full_name_list.append(page[j])
    
    full_name = " ".join(full_name_list)
    
    if full_name in PLAYER_NAME_CLEANUP.keys():
        full_name = PLAYER_NAME_CLEANUP.get(full_name)

    return full_name
    
def fill_last_7_fields(dictionary: dict, page: list, current_index:int, date, full_name):
    dictionary['average_points'].append(float(page[current_index]))
    dictionary['total_points'].append(float(page[current_index+1]))
    dictionary['points_lost_this_year'].append(float(page[current_index+3]))
    dictionary['week_of'].append(date)
    
    try:
        dictionary['player_id'].append((PLAYER_ID_DICT[full_name].get('player_id')))
        # print(full_name," : ",(PLAYER_ID_DICT[full_name].get('player_id')) )
    except KeyError:
        dictionary['player_id'].append(-99)
        # print(full_name," : ","-99")

    try:
        dictionary['events_played_div'].append(int(page[current_index+2]))
    except ValueError:
        dictionary['events_played_div'].append(-99)   
    try:
        dictionary['points_won_this_year'].append(float(page[current_index+4]))
    except ValueError:
        dictionary['points_won_this_year'].append(float(0))
    try:
        dictionary['events_played_act'].append((page[current_index+5]))
    except IndexError:
        dictionary['events_played_act'].append(-99)
    

# ******* READ PDF, CREATE CSV, INSERT INTO DB *********
# ******************************************************  
  
for file_num, filename in enumerate(os.listdir("owgr_pdfs")[:]):
    print(f"************ {file_num} ************\n********{filename[:-4]}*******")
    owgr_dict = {
        'this_week':[],
        'last_week':[],
        'end_prev_year':[],
        'full_name':[],
        'country':[],
        'average_points':[],
        'total_points':[],
        'events_played_div':[],
        'points_lost_this_year':[],
        'points_won_this_year':[],
        'events_played_act':[],
        'week_of':[],
        'player_id':[],

    }

    file_match = PDF_FILENAME_PATTERN.search(filename)
    week_of = datetime.date.fromisocalendar(int(file_match.group('year')),int(file_match.group('week')),7)

    for page_num, page in enumerate(read_pdf(f"{PDF_FILEPATH}{filename}")[:6]):
        country_count = 0
        # print(page)
        for i, word in enumerate(page):
            country_type = None
            if ROW_START_PATTERN.search(word):
                owgr_dict['this_week'].append(int(page[i-1]))
                owgr_dict['last_week'].append(int(clean_week_strings(page[i])))
                try:
                    owgr_dict['end_prev_year'].append(int(clean_week_strings(page[i+1])))
                except ValueError:
                    owgr_dict['end_prev_year'].append(-99)
                end_prev_year_index = i+1

            # Three word country
            if AVG_POINT_PATTERN.search(word) and page[i-1] in COUNTRY_CONCAT_WORDS_FOR_OWGR and page[i-2] in COUNTRIES_FOR_OWGR and page[i-3] in COUNTRY_PREFIX_FOR_OWGR:
                country_count +=1
                # print(f"three-word country: {page[i-2]} {page[i-1]} : {country_count}")
                owgr_dict['country'].append(f"{page[i-3]} {page[i-2]}")
                full_name = clean_full_name(end_prev_year_index + 1, i-3)
                owgr_dict['full_name'].append(full_name)
                fill_last_7_fields(owgr_dict, page, i, week_of.strftime("%Y-%m-%d"),full_name)


            # Two word country
            if AVG_POINT_PATTERN.search(word) and page[i-1] in COUNTRIES_FOR_OWGR and page[i-2] in COUNTRY_PREFIX_FOR_OWGR:
                country_count +=1
                # print(f"two-word country: {page[i-2]} {page[i-1]} : {country_count}")
                owgr_dict['country'].append(f"{page[i-2]} {page[i-1]}")
                full_name = clean_full_name(end_prev_year_index + 1, i-2)
                owgr_dict['full_name'].append(full_name)
                fill_last_7_fields(owgr_dict, page, i, week_of.strftime("%Y-%m-%d"), full_name)
    

            # One word country
            if AVG_POINT_PATTERN.search(word) and page[i-1] in COUNTRIES_FOR_OWGR and page[i-2] not in COUNTRY_PREFIX_FOR_OWGR: 
                country_count +=1
                # print(f"one-word country: {page[i-1]} : {country_count}")
                if page[i-1] in COUNTRY_NAME_MAP.keys():
                    owgr_dict['country'].append(COUNTRY_NAME_MAP.get(page[i-1]))
                else:
                    owgr_dict['country'].append(page[i-1])
                
                full_name = clean_full_name(end_prev_year_index + 1, i-1)
                owgr_dict['full_name'].append(full_name)
                fill_last_7_fields(owgr_dict, page, i, week_of.strftime("%Y-%m-%d"), full_name)
            


    csv_filename = f"{CSV_FILEPATH}{filename[:-4]}.csv"
    owgr_df = pd.DataFrame(owgr_dict)

    data = list(owgr_df.itertuples(index=False, name=None))
    # print(data)
    owgr_df = owgr_df.astype({'player_id':'int'})
    # owgr_df.to_csv(csv_filename, index=False, header=False)
    


    with Database(db_type='prod') as (con, cur):
        cur.executemany(OWGR_INSERT_QUERY, data)
        con.commit()
    


