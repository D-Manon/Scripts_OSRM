import psycopg2
import os
import sys
sys.path.insert(0,"/home/manon/Documents/Scripts/src")
from src.env import EnvVar


def change_maxspeeds(db_name, db_password, env_geo, pth_folder_data, pth_scripts):
    """
    Cette fonction réalise d'abord une intersection pour attribuer un environnement urbain à chaque tronçon OSM. Le type d'environnement urbain attribué est celui que le tronçon parcourt le plus au total. Elle exécute ensuite un script SQL qui manipule le format hstore des données OSM pour changer les valeurs du tag maxspeed selon l'environnement urbain traversé.

    - db_name : nom de la bdd
    - db_password : mot de passe pour accéder à la bdd
    - env_geo : nom du fichier vectoriel des environnements urbains (sans l'extension)
    - pth_folder_data : chemin d'accès vers le répertoire contenant le fichier gpkg des environnements urbains et les données OSM non modifiées
    - pth_scripts : chemin d'accès vers le répertoire contenant les scripts dont change_maxspeeds.sql
    """
    
    try:
        db_host = EnvVar.connexion_pg['db_host']
        db_port = EnvVar.connexion_pg['db_port']
        db_user = EnvVar.connexion_pg['db_user']
        
        cmd_import_gpkg_postgis = f"ogr2ogr -f PostgreSQL PG:\"dbname='{db_name}' host={db_host} port={db_port} user={db_user} password={db_password}\" {pth_folder_data}{env_geo}.gpkg"
        os.system(cmd_import_gpkg_postgis)
        
        con = psycopg2.connect(dbname=db_name, user=db_user, host=db_host, password=db_password)

        cur = con.cursor()
        # Attribution d'un environnement géo à chaque tronçon par intersection
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
        # Changement des maxspeeds OSM
        cur.execute(open(f"{pth_scripts}change_maxspeeds.sql", "r").read())
        con.commit()
        con.close()
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    change_maxspeeds(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
