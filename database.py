from os import environ as env
from dotenv import load_dotenv
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor

load_dotenv()

class Database:
    def __init__(self, db_type='prod') -> None:
        self.conn = None
        self.cursor = None
        self.host = env.get("HOST")

        if db_type.lower() == 'dev':
            self.database = env.get("DBNAME_DEV")
        elif db_type.lower() == 'prod':
            self.database = env.get("DBNAME")
        else:
            raise ValueError("Enter a valid environment name (prod/dev)")
        
        self.user = env.get("USERNAME")
        self.password = env.get("PASSWORD")
        self.port = env.get("PORT")


    def __enter__(self):
        self.open()
        return (self, self.conn, self.cursor)


    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    def open(self):
        self.conn = connect(
            host = self.host,
            dbname = self.database,
            user = self.user,
            password = self.password,
            port = self.port
        )

        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)      
           

    def close(self):
        self.cursor.close()
        self.conn.close()


    def write(self, table: str, columns: list[str], values: list, return_key: str):
        insert_string = """
        INSERT INTO {} ({}) VALUES
        ({}) RETURNING {}      
        """
        self.cursor.execute(sql.SQL(insert_string).format(
            sql.Identifier(table), 
            sql.SQL(",").join(map(sql.Identifier, columns)),
            sql.SQL(",").join(map(sql.Literal, values)),
            sql.Identifier(return_key)
            ))
        
        results = self.cursor.fetchone().get(return_key)              
     
        return results
    

    def create_table(self, table: str, columns: list[str], column_type: list):

        set_columns = (sql.SQL("{} {}").format(
            sql.Identifier(item[0]),
            sql.SQL(item[1])
        ) for item in list(zip(columns, column_type)))

        join_column_def = sql.SQL(",").join(set_columns)

        query = sql.SQL("""CREATE TABLE IF NOT EXISTS {} ({})""").format(
            sql.Identifier(table),
            join_column_def
            
        )

        print(query.as_string(self.conn))
        self.cursor.execute(query)
        self.conn.commit()