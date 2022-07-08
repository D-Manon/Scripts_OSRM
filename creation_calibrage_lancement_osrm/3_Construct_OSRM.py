import os
import shutil
import sys


def construct_osrm(network, profile, algorithm, path_build='/srv/osrm/build/', path_profiles='/srv/osrm/osrm-backend/profiles/'):
    """
    Construction du réseau OSRM : extraction du réseau depuis un pbf avec le profil spécifié pour les vitesses, création et organisation des dossiers
    contenant les différents fichiers résultats, étapes de construction selon l'agorithme spécifié.
    
    - network : nom du fichier réseau pbf, sans l'extension
    - profile : nom du profil à utiliser, sans l'extenstion, ie car ou car_clc
    - algorithm : algorithme du plus court chemin ie CH ou MLD
    """
    
    os.chdir('/home/manon/Documents/BDD/OSM')
    path_data_folder = os.getcwd() + '/'
    algorithm = algorithm.lower()
    path_data = f"{path_data_folder}{network}/{profile}/{algorithm}/"

    os.mkdir(network) if not os.path.isdir(network) else print(f"Le fichier {network} existe déjà")
    os.mkdir(f'{network}/{profile}') if not os.path.isdir(f'{network}/{profile}') else print(f"Le fichier {profile} existe déjà")
    os.mkdir(path_data) if not os.path.isdir(path_data) else print(f"Le fichier {algorithm} existe déjà")
    
    cmd_osmium = f"osmium add-locations-to-ways --verbose --keep-untagged-nodes --ignore-missing-nodes --overwrite -o {path_data}{network}_with_geom.osm.pbf {path_data_folder}{network}.osm.pbf"
    os.system(cmd_osmium)

    cmd_extract = f'{path_build}osrm-extract -p {path_profiles}{profile}.lua {path_data}{network}_with_geom.osm.pbf --with-osm-metadata'
    os.system(cmd_extract)

    list_files = os.listdir(path_data_folder)
    for file in list_files:
        if not file.endswith(('.pbf', '.ipynb')):
            if not os.path.isdir(file):
                shutil.move(f"{path_data_folder}{file}", f"{path_data}{file}")
                

    if algorithm == "ch":
        cmd_contract = f'{path_build}osrm-contract "{path_data}{network}_with_geom.osrm"'
        os.system(cmd_contract)

    elif algorithm == "mld":
        cmd_partition = f'{path_build}osrm-partition {path_data}{network}_with_geom.osrm'
        os.system(cmd_partition)

        cmd_customize = f'{path_build}osrm-customize {path_data}{network}_with_geom.osrm'
        os.system(cmd_customize)

    else:
        print("Entrer l'algorithme du plus court chemin 'MLD' ou 'CH' comme troisième argument")
        

        
def main():
    try:
        construct_osrm(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main()
