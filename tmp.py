from database import Database
from psycopg2 import connect, sql

with Database(db_type='dev') as (db, con, cur):
    table_name = 'test'
    col_query = """
    SELECT * 
    FROM  information_schema.columns 
    WHERE table_schema = %s 
    and table_name = %s
    order by
    ordinal_position
    """
    
    print(cur.execute(col_query, ("public", table_name)))
    results = cur.fetchall()



print([result.get("column_name") for result in results])

with Database(db_type='dev') as (db, con, cur):
    query = sql.SQL("""SELECT 1 FROM {}""").format(
    sql.Identifier('doesntexist'))

    cur.execute(query)
    print(cur.fetchall())
