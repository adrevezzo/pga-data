from os import environ as env
from dotenv import load_dotenv
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor

load_dotenv()

class Database:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None
        self.host = env.get("HOST")
        self.database = env.get("DBNAME")
        self.user = env.get("USERNAME")
        self.password = env.get("PASSWORD")
        self.port = env.get("PORT")


    def open(self):
        self.conn = connect(
            host = self.host,
            dbname = self.database,
            user = self.user,
            password = self.password,
            port = self.port
        )

        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        return self.conn, self.cursor
           

    def close(self):
        self.cursor.close()
        self.conn.close()


    def write(self, table: str, columns: list[str], values: list, return_key: str):
        self.open()
        with self.conn as conn:
            with self.cursor as cur:
                insert_string = """
                INSERT INTO {} ({}) VALUES
                ({}) RETURNING {}      
                """
                cur.execute(sql.SQL(insert_string).format(
                    sql.Identifier(table), 
                    sql.SQL(",").join(map(sql.Identifier, columns)),
                    sql.SQL(",").join(map(sql.Literal, values)),
                    sql.Identifier(return_key)
                    ))
                
                results = cur.fetchone().get(return_key)              
        self.close()       
        return results