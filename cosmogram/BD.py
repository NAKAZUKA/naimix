from pprint import pprint

import psycopg2
import settings as conf


def get_db_connection():
    conn = psycopg2.connect(host=conf.GET('host_postgres'),
                            database=conf.GET('database'),
                            user=conf.GET('user'),
                            password=conf.GET('password'))
    return conn

def get_question(sqll):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sqll)
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

pprint(get_question("SELECT * FROM pg_catalog.pg_tables;"))