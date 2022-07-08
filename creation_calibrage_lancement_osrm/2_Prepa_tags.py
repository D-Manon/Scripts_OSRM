import psycopg2
import os
import sys


def main(bdd_name, env_geo, password):
    try:
        
        cmd_import_gpkg_postgis = f"ogr2ogr -f PostgreSQL PG:\"dbname='{bdd_name}' host='localhost' port='5432' user='manon' password={password}\" /home/manon/Documents/BDD/{env_geo}.gpkg"
        os.system(cmd_import_gpkg_postgis)
        
        con = psycopg2.connect(dbname=bdd_name, user='manon', host='localhost', password='Stage2022')

        cur = con.cursor()
        # Attribution d'un environnement géo à chaque tronçon (selon critère de longueur max du morceau de tronçon qui traverse un environnement)
        tab_env_geo = env_geo
        cur.execute(''' 
            CREATE TABLE tmp_env_geo AS
            SELECT DISTINCT ON (id) id, sum_longueur_inter_m, FIRST_VALUE(env_geo) OVER(PARTITION BY id ORDER BY id, sum_longueur_inter_m desc) env_geo_max
            FROM (
                SELECT id, sum(longueur_inter_m) as sum_longueur_inter_m, env_geo
                FROM (
                    SELECT  ways.id, ST_Length(ST_Transform(ST_Intersection(geom, linestring),3857))::INTEGER as longueur_inter_m, env_geo
                    FROM %s, ways
                    WHERE ST_Length(linestring) > 0 AND ST_Intersects(geom, linestring)
                    GROUP BY ways.id, geom, env_geo) as tab_longueurs
                GROUP by id, env_geo) as sum_longueur
            ORDER BY id, sum_longueur_inter_m;
        ''' % tab_env_geo)
        con.commit()
        cur.execute(open("/home/manon/Documents/Scripts/prepa_tags.sql", "r").read())
        con.commit()
        con.close()
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

    