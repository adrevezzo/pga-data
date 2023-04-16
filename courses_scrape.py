import time
from database import Database
from graphql import GraphQLQuery
from psycopg2.errors import UniqueViolation

gql = GraphQLQuery()

tournaments_without_course = []
courses_added = []

with Database(db_type='dev') as (db, con, cur):
    select_tournament_ids = """
    SELECT
    id,
    pga_tournament_id
    FROM tournaments
    WHERE year = '2023'
    """

    cur.execute(select_tournament_ids)
    results = cur.fetchall()

    for result in results:
        # print(result)
        insert_course_data = """
        INSERT INTO courses (
            course_name,
            course_id_pga,
            city,
            state,
            country
        )
        
        VALUES
        (%s, %s, %s, %s, %s)
        
        """
        time.sleep(7)  
        all_data = gql.scrape_courses(result.get('pga_tournament_id'))

        try:
            tournament_data = all_data['data']['tournaments'][0]
        except TypeError:
            tournaments_without_course.append(result.get('pga_tournament_id'))
        else:
            
            for course in tournament_data['courses']:
                if course['id'] in courses_added:
                    continue
                else:
                    course_name = course['courseName']
                    course_id_pga = course['id']
                    city = tournament_data['city']
                    state = tournament_data['state']
                    country = tournament_data['country']

                    data_completed = (
                        course_name, 
                        course_id_pga,
                        city,
                        state,
                        country
                        )

                    try:
                        cur.execute(insert_course_data, data_completed)
                    except UniqueViolation:
                        print(f"Course {course_name} already in database")
                        con.rollback()
                    else:
                        print(f"Course {course_name} added to database")
                        con.commit()
                        courses_added.append(course_id_pga)




