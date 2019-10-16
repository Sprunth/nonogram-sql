import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Connected to db: {sqlite3.version}')
        return conn
    except Error as e:
        print(e)
 
def create_Table(conn, create_sql):
    try:
        c = conn.cursor()
        c.execute(create_sql)
    except Error as e:
        print(e)

if __name__ == '__main__':
    create_connection(r"nonogram.db")
