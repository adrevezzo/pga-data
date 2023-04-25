import time
import json
from database import Database
from graphql import GraphQLQuery
from utils import get_column_names
from psycopg2 import sql
from psycopg2.errors import UniqueViolation, UndefinedTable

gql = GraphQLQuery()

with open("stat_id_dictionary.json") as stat_list:
    all_stats = json.load(stat_list)
 
# with open("sg_tot_example.json") as stat_example:
#     ex = json.load(stat_example)

with Database(db_type='prod') as (db, con, cur):
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
    AND lower(tournament_name) NOT LIKE 'zurich classic%'
    order by tournament_end_date desc  
    """
    cur.execute(thru_tourn_select)
    thru_tourn_results = cur.fetchall()

player_id_dict = {result.get("pga_id"):int(result.get("id")) for result in player_id_results }
tournament_id_dict = {result.get("pga_tournament_id"):int(result.get("id")) for result in tournament_id_results }
thru_tourn_list = [result.get("pga_tournament_id") for result in thru_tourn_results]

with Database(db_type='prod') as (db, con, cur):
    for tournament in thru_tourn_list:
        print(tournament)
        for stat in list(all_stats.keys())[:10]:        
            print(all_stats.get(stat))
            table_name = all_stats.get(stat)

            time.sleep(6)
            stats = gql.scrape_stats(stat_id=stat, schedule_year=2023, through_event_flag="THROUGH_EVENT", pga_tournament_id=tournament)
            
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
                req_num_stats = len(cols)
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

                        if len(row_vals) < req_num_stats:
                            i = 0
                            for i in range(req_num_stats-len(row_vals)):
                                row_vals.append(None)
                                i += 1

                        vals.append(tuple(row_vals))

                try:
                    db.bulk_insert(table_name, cols, vals)
                except UniqueViolation:
                    print("Already in Database")
                    con.rollback()
                    continue