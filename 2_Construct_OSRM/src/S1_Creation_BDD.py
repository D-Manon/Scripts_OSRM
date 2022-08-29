import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from src.env import EnvVar

def create_db(db_name, db_password, pth_osmosis_scripts):
    """
    Cette fonction crée la base de données postgres avec les extensions postgis et hstore et met en place la structure adéquate des tables grâce aux scripts sql osmosis. La bdd stockera les données routières OSM et permettra de changer les vitesses de parcours des tronçons conformément à la méthodologie d'Odomatrix.

    - db_name : nom de la bdd
    - db_password : mot de passe pour accéder à la bdd
    - pth_osmosis_scripts : chemin d'accès vers les scripts osmosis préparant les tables
    """

    try:
        db_superuser = EnvVar.connexion_pg['db_superuser']
        db_superpassword = EnvVar.connexion_pg['db_superpassword']
        db_superdb = EnvVar.connexion_pg['db_superdb']
        db_host = EnvVar.connexion_pg['db_host']
        db_user = EnvVar.connexion_pg['db_user']

        con = psycopg2.connect(dbname=db_superdb, user=db_superuser, host=db_host, password=db_superpassword)

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        sql_create = f"""CREATE DATABASE {db_name} OWNER {db_user}"""
        cur.execute(sql_create)
        con.close()

        con = psycopg2.connect(dbname=db_name,
                               user=db_superuser, host=db_host,
                               password=db_superpassword)

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION hstore;')
        con.close()

        con = psycopg2.connect(dbname=db_name,
                               user=db_user, host=db_host,
                               password=db_password)

        cur = con.cursor()
        cur.execute(open(f"{pth_osmosis_scripts}pgsnapshot_schema_0.6.sql", "r").read())
        cur.execute(open(f"{pth_osmosis_scripts}pgsnapshot_schema_0.6_action.sql", "r").read())
        cur.execute(open(f"{pth_osmosis_scripts}pgsnapshot_schema_0.6_bbox.sql", "r").read())
        cur.execute(open(f"{pth_osmosis_scripts}pgsnapshot_schema_0.6_linestring.sql", "r").read())
        con.commit()
        con.close()

    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    create_db(sys.argv[1], sys.argv[2], sys.argv[3])
