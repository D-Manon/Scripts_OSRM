"""
Lance successivement des scripts python et des lignes de commandes bash pour construire le distancier avec OSRM :
# PREPARATION DES DONNEES : 1) création BDD, 2) téléchargement des données OSM, 3) sélection des highways OSM souhaités,
4) import dans bdd, 5) changement des maxspeeds selon l'environnement urbain, 6) export des données modifiées en pbf
# CREATION DU RESEAU : 7) construction du réseau OSRM a partir des données précédemment configurées

- env_geo :nom du fichier vectoriel des environnements urbains, sans l'extension
- network : nom du fichier réseau pbf, sans l'extension
- profile : nom du profil à utiliser, sans l'extension, ie car ou car_updated1
- algorithm : algorithme du plus court chemin ie CH ou MLD
"""

import os
# import sys
# from importlib import reload
# reload(Timer) --> si non mise à jour de utils.py
import src.utils as Timer
from src.S1_Creation_BDD import create_db
from src.S2_Configuration_vitesses import change_maxspeeds
from src.S3_Construction_OSRM import construct_osrm
from src.env import EnvVar

# Chemins d'accès
pth_main_folder = EnvVar.paths['pth_main_folder']
pth_folder_osmosis = EnvVar.paths['pth_folder_osmosis']
pth_folder_osrm = EnvVar.paths['pth_folder_osrm']

# Options
env_geo = EnvVar.options['env_geo']
network = EnvVar.options['network']
algorithm = EnvVar.options['algorithm'].lower()
profile = EnvVar.options['profile']


def main(env_geo, network, profile, algorithm):
    try:
        # Chargement des variables de chemins d'accès
        pth_scripts = EnvVar.paths['pth_scripts']
        pth_folder_data = EnvVar.paths['pth_folder_data']
        pth_folder_results = EnvVar.paths['pth_folder_results']
        os.chdir(pth_folder_results)
        pth_results_network = EnvVar.paths['pth_results_network']
        pth_osmosis_scripts = EnvVar.paths['pth_osmosis_scripts']
        pth_osmosis = EnvVar.paths['pth_osmosis']
        pth_osrm_build = EnvVar.paths['pth_osrm_build']
        pth_osrm_profiles = EnvVar.paths['pth_osrm_profiles']
        url_network = EnvVar.options['url_network']

        # Chargement des variables de connexion postgres
        db_host = EnvVar.connexion_pg['db_host']
        db_name = EnvVar.connexion_pg['db_name']
        db_user = EnvVar.connexion_pg['db_user']
        db_password = EnvVar.connexion_pg['db_password']

        # Création des dossiers qui contiendront le réseau
        os.mkdir(network) if not os.path.isdir(network) else print(f"Le dossier {network} existe déjà")
        os.mkdir(f'{network}/{profile}') if not os.path.isdir(f'{network}/{profile}') else print(f"Le dossier {profile} existe déjà")
        os.mkdir(pth_results_network) if not os.path.isdir(pth_results_network) else print(f"Le dossier {algorithm} existe déjà")
        
        # Pour créer un nouveau document texte à chaque fois que le script est lancé en écrasant le précédent document du même nom (n'ajoute pas les nouveaux temps à la suite)
        file = open(f"{pth_folder_results}tps_creation_reseau.txt","w")
        file.close()
        
        # Instanciation de la classe Timer
        t=Timer.Timer()

        ## PREPARATION DES DONNEES
        # 1 - Création BDD
        t.start()
        create_db(db_name, db_password, pth_osmosis_scripts)
        t.stop_write_close('1. Création BDD', pth_folder_results)
        
        # 2 - Téléchargement des données OSM si elles ne sont pas déjà téléchargées
        t.start()
        os.system(f"wget -P {pth_folder_data} {url_network}") if not os.path.isfile(f"{pth_folder_data}{network}.osm.pbf") else print(f"Le fichier {network}.osm.pbf a déjà été téléchargé")
        t.stop_write_close('2. Téléchargement des données OSM', pth_folder_results)
        
        # 3 - Sélection et extraction des highways des données OSM
        t.start()
        os.system(f"{pth_osmosis} --read-pbf {pth_folder_data}{network}.osm.pbf --tf accept-ways highway=motorway,trunk,primary,secondary,tertiary,unclassified,residential,motorway_link,trunk_link,primary_link,secondary_link,tertiary_link,road,unclassified --used-node --write-pbf {pth_results_network}{network}_highways.osm.pbf")
        t.stop_write_close('3. Extraction des highways', pth_folder_results)       
        
        # 4 - Chargement des highways dans postgis
        t.start()
        os.system(f"{pth_osmosis} --read-pbf {pth_results_network}{network}_highways.osm.pbf --log-progress --write-pgsql database={db_name} user={db_user} password={db_password}")
        t.stop_write_close('4. Chargement des highways dans postgis', pth_folder_results)         
        
        # 5 - Attribution des vitesses selon l'environnement urbain
        t.start()
        change_maxspeeds(db_name, db_password, env_geo, pth_folder_data, pth_scripts)
        t.stop_write_close("5. Attribution des vitesses selon l'environnement urbain", pth_folder_results) 
        
        # 6 - Exportation des highways modifiés depuis postgis
        t.start()
        os.system(f"{pth_osmosis} --read-pgsql host={db_host} database={db_name} user={db_user} password={db_password} --dataset-dump --write-pbf {pth_results_network}{network}_updated.osm.pbf")
        t.stop_write_close('6. Exportation des highways modifiés depuis postgis', pth_folder_results)

        ## CREATION RESEAU
        # 7 - Construction du réseau OSRM
        t.start()
        construct_osrm(f"{network}_updated", profile, algorithm, pth_osrm_build, pth_osrm_profiles, pth_folder_results, pth_results_network)
        t.stop_write_close("7. Construction du réseau OSRM", pth_folder_results)
        
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main(env_geo, network, profile, algorithm)
