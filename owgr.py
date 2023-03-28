import os
import re
from PyPDF2 import PdfReader
import pandas as pd
from utils import COUNTRIES_FOR_OWGR, COUNTRY_PREFIX_FOR_OWGR
import datetime


def read_pdf(pdf_file):
    text = ''
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
    return " ".join(full_name_list)
    
def fill_last_6_fields(dictionary: dict, page: list, current_index:int, date):
    dictionary['average_points'].append(page[current_index])
    dictionary['total_points'].append(page[current_index+1])
    dictionary['events_played_div'].append(page[current_index+2])
    dictionary['points_lost_this_year'].append(page[current_index+3])
    dictionary['points_won_this_year'].append(page[current_index+4])
    dictionary['events_played_act'].append(page[current_index+5])
    dictionary['week_of'].append(date)





filepath = 'owgr_pdfs/'

row_start_pattern = re.compile(r'^\([0-9]+\)$')
avg_point_pattern = re.compile(r'^[0-9]+\.[0-9]+$')
pdf_filename_pattern = re.compile(r'^owgr(?P<week>[0-9]{2})f(?P<year>[0-9]{4}).pdf$')

end_prev_year_index = None
country_count = 0

for filename in os.listdir("owgr_pdfs")[:2]:
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
        'week_of':[]
    }

    file_match = pdf_filename_pattern.search(filename)
    week_of = datetime.date.fromisocalendar(int(file_match.group('year')),int(file_match.group('week')),7)

    for page in read_pdf(f"{filepath}{filename}"):
        for i, word in enumerate(page):
            country_type = None
            if row_start_pattern.search(word):
                owgr_dict['this_week'].append(page[i-1])
                owgr_dict['last_week'].append(clean_week_strings(page[i]))
                owgr_dict['end_prev_year'].append(clean_week_strings(page[i+1]))
                end_prev_year_index = i+1

            # Two word country
            if avg_point_pattern.search(word) and page[i-1] in COUNTRIES_FOR_OWGR and page[i-2] in COUNTRY_PREFIX_FOR_OWGR:
                # country_count +=1
                # print(f"two-word country: {page[i-2]} {page[i-1]} : {country_count}")
                owgr_dict['country'].append(f"{page[i-2]} {page[i-1]}")
                owgr_dict['full_name'].append(clean_full_name(end_prev_year_index + 1, i-2))
                fill_last_6_fields(owgr_dict, page, i, week_of.strftime("%Y-%m-%d"))
    

            # One word country
            if avg_point_pattern.search(word) and page[i-1] in COUNTRIES_FOR_OWGR and page[i-2] not in COUNTRY_PREFIX_FOR_OWGR: 
                # country_count +=1
                # print(f"one-word country: {page[i-1]} : {country_count}")
                if page[i-1] == "Venezuala":
                    owgr_dict['country'].append("Venezuela")
                else:
                    owgr_dict['country'].append(page[i-1])
                owgr_dict['full_name'].append(clean_full_name(end_prev_year_index + 1, i-1))
                fill_last_6_fields(owgr_dict, page, i, week_of.strftime("%Y-%m-%d"))

                    
    owgr_df = pd.DataFrame(owgr_dict)
    print(owgr_df.head(10),"\n", owgr_df.tail(10))

