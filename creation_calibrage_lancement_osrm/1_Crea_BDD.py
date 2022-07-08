import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
import pandas as pd
import os
import sys

def main(bdd_name, pth_scripts_osmosis, password):
    try:
        con = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='user')

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
        cur = con.cursor()
        sql_create = f"""CREATE DATABASE {bdd_name} OWNER manon"""
        cur.execute(sql_create)
        con.close()

        con = psycopg2.connect(dbname=bdd_name,
              user='postgres', host='localhost',
              password='user')

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
        cur = con.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION hstore;')
        con.close()

        con = psycopg2.connect(dbname=bdd_name,
              user='manon', host='localhost',
              password=password)

        cur = con.cursor()
        cur.execute(open(f"{pth_scripts_osmosis}pgsnapshot_schema_0.6.sql", "r").read())
        cur.execute(open(f"{pth_scripts_osmosis}pgsnapshot_schema_0.6_action.sql", "r").read())
        cur.execute(open(f"{pth_scripts_osmosis}pgsnapshot_schema_0.6_bbox.sql", "r").read())
        cur.execute(open(f"{pth_scripts_osmosis}pgsnapshot_schema_0.6_linestring.sql", "r").read())
        con.commit()
        con.close()
    
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
