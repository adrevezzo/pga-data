import time
import json
from database import Database
import queries
from graphql import GraphQLQuery

gql = GraphQLQuery()

YEARS = ["2013","2014","2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
# YEARS = ['2023']


for year in YEARS:
    print(f"Running {year} Query")
    
    time.sleep(10)   
    all_data = gql.scrape_schedule(schedule_year=year)

    data_completed = all_data['data']['schedule']['completed']
    data_upcoming = all_data['data']['schedule']['upcoming']
    season = all_data['data']['schedule']['seasonYear']
  
    with Database(db_type='dev') as (db, con, cur):
        for status in (data_completed, data_upcoming):
            for tournament_month in status:
                month = tournament_month['month']
                year = tournament_month['year']
                for tournament in tournament_month['tournaments']:
                    pga_tournament_id = tournament['id']
                    tournament_name = tournament['tournamentName']
                    tournament_num = (pga_tournament_id[-3:])
                    first_place_earnings = tournament['championEarnings']
                    purse = tournament['purse']
                    city = tournament['city']
                    state = tournament['state']
                    country = tournament['country']
                    course = tournament['courseName']

                    data_completed = (
                        pga_tournament_id, 
                        tournament_name,
                        tournament_num, 
                        first_place_earnings, 
                        purse, 
                        city,
                        state,
                        country, 
                        course,
                        month,
                        year,
                        season
                        )
                    cur.execute(queries.SCHEDULE_INSERT_QUERY, data_completed)
                    con.commit()

    