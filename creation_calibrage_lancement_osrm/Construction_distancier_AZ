import os
import sys
from datetime import datetime


def main(bdd_name, env_geo, network, profile, algorithm, pth_scripts_osmosis, password, pth_osmosis, path_build, path_profiles):
    try:
        cmd1_crea_BDD = ["1. Création BDD", f"python3 /home/manon/Documents/Scripts/1_Crea_BDD.py {bdd_name} {pth_scripts_osmosis} {password}"]
        cmd2_extract_highways = ["2. Extraction des highways", f"{pth_osmosis} --read-pbf /home/manon/Documents/BDD/OSM/{network}.osm.pbf --tf accept-ways highway=* --tf reject-ways highway=bridleway,bus_stop,construction,cycleway,footway,living_street,path,pedestrian,proposed,raceway,rest_area,service,services,steps,via_ferrata,track,bus_guideway,platform,abandoned,elevator,corridor,access,busway,disused,crossing,emergency_access_point,emergency_bay,escape,flat_steps,industrial,milestone,passing_place,razed,stairs,stop,street_lamp,traffic_signals,trailhead,yes --used-node --write-pbf /home/manon/Documents/BDD/OSM/{network}_highways.osm.pbf"]
        cmd3_load_postgis = ["3. Chargement des highways dans postgis", f"{pth_osmosis} --read-pbf /home/manon/Documents/BDD/OSM/{network}_highways.osm.pbf --log-progress --write-pgsql database={bdd_name} user='manon' password={password}"]
        cmd4_prepa_tags = ["4. Attribution des vitesses selon l'environnement géographique", f"python3 /home/manon/Documents/Scripts/2_Prepa_tags.py {bdd_name} {env_geo} {password}"]
        cmd5_export_from_postgis = ['5. Exportation des highways modifiés depuis postgis', f"{pth_osmosis} --read-pgsql host='localhost' database={bdd_name} user='manon' password={password} --dataset-dump --write-pbf /home/manon/Documents/BDD/OSM/{network}_updated.osm.pbf"]
        cmd6_construct_osrm = ['6. Construction du réseau OSRM', f"python3 /home/manon/Documents/Scripts/3_Construct_OSRM.py {network}_updated {profile} {algorithm} {path_build} {path_profiles}"]

        list_etapes = [cmd1_crea_BDD, cmd2_extract_highways, cmd3_load_postgis, cmd4_prepa_tags, cmd5_export_from_postgis, cmd6_construct_osrm]

        file = open(f"/home/manon/Documents/Scripts/tps_execution_script_{network}_{algorithm}.txt","w")
        file.close()

        for etape in list_etapes:
            print(etape[0])
            start = datetime.now()
            os.system(etape[1])
            end = datetime.now()
            lines = ['', etape[0], f"Début : {start} ; Fin : {end} ; Temps d'exécution : {end-start} \n"]
            file = open(f'/home/manon/Documents/Scripts/tps_execution_script_{network}_{algorithm}.txt', 'a')
            file.writelines('\n'.join(lines))
            file.close()
            
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], pth_scripts_osmosis="/home/manon/osmosis/script/", password=password, pth_osmosis="/home/manon/osmosis/bin/osmosis", path_build='/srv/osrm/build/', path_profiles='/srv/osrm/osrm-backend/profiles/')
