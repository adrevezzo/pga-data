from database import Database
import time
import queries
from psycopg2.errors import UniqueViolation
from graphql import GraphQLQuery

gql = GraphQLQuery()

# Static data for testing
# with open("player_results_by_year.json") as data:
#     all_data = json.load(data)

with Database(db_type='dev') as (db, con, cur):
    get_players_query = """
    SELECT 
    first_name || ' ' || last_name as player_name
    ,pga_id 
    FROM players
    """
    cur.execute(get_players_query)
    results = cur.fetchall()
print(con.closed, " ", cur.closed)

all_players = [(result.get("pga_id"),result.get("player_name")) for result in results]

for player in all_players[0:6]:
    all_data = gql.scrape_results(schedule_year=2023, pga_player_id=player[0])

    years_active = []
    tour_list = all_data['data']['playerProfileSeasonResults']['seasonPills']
    for tour in tour_list:
        if tour.get("tourCode") == "R":
            for year in tour.get("years"):
                years_active.append(year.get("year")) 
   
    for year in years_active:
        
        if int(year) <2023:
            print(f"Player: {player[1]}, Year: {year} - skipping")
            continue
        else:
            print(f"Player: {player[1]}, Year: {year}")

            time.sleep(7)
            all_data = gql.scrape_results(schedule_year=year, pga_player_id=player[0])

            with Database(db_type='dev') as (db, con, cur):
                query_id = all_data['data']['playerProfileSeasonResults']['playerId']
                cur.execute(queries.PLAYER_ID_SELECT, (query_id,))
                result = cur.fetchone()
                player_id = result.get("id")

                tournaments = all_data['data']['playerProfileSeasonResults']['tournaments']
                for tournament in tournaments:
                    pga_tournament_id = tournament['tournamentId']

                    cur.execute(queries.TOURNAMENT_ID_SELECT, (pga_tournament_id,))
                    result = cur.fetchone()
                    
                    if not result:
                        continue
                    else:
                        tournament_id = result.get("id")
                        
                        tournament_end_date = tournament['tournamentEndDate']
                        finish_position = tournament['finishPosition']
                        
                        r1 = tournament['r1'] if tournament['r1'] != "-" else None
                        r2 = tournament['r2'] if tournament['r2'] != "-" else None
                        r3 = tournament['r3'] if tournament['r3'] != "-" else None
                        r4 = tournament['r4'] if tournament['r4'] != "-" else None
                        total = tournament['total'] if tournament['total'] != "" else None
                        to_par = tournament['toPar']
                        points_rank = tournament['pointsRank'] if tournament['pointsRank'] != "-" else None
                        tournament_points = tournament['points'] if tournament['points'] != "-" else None

                        data_completed = (
                            player_id, 
                            tournament_id,
                            tournament_end_date, 
                            finish_position, 
                            r1, 
                            r2,
                            r3,
                            r4, 
                            total,
                            to_par,
                            points_rank,
                            tournament_points
                            )
                        
                        try:
                            cur.execute(queries.PLAYER_RESULTS_INSERT_QUERY, data_completed)

                        except UniqueViolation:
                            print(f'Player: {player[1]}, Tournament {tournament_id} Already in database')
                            con.rollback()
                        else:
                            print(f'Player: {player[1]}, Tournament {tournament_id} Added to database')
                            con.commit()

