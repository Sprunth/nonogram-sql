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
 
def db_execute(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def db_execute_with_task(conn, sql, task):
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

if __name__ == '__main__':
    create_connection(r"nonogram.db")
