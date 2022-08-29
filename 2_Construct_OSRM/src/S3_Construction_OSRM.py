import os
import shutil
import sys

        
def construct_osrm(network, profile, algorithm, pth_osrm_build, pth_osrm_profiles, pth_folder_results, pth_results_network): 
    """
    Construction du réseau OSRM : extraction du réseau depuis un pbf avec le profil spécifié pour les vitesses, création et organisation des dossiers contenant les différents fichiers résultats, étapes de construction selon l'algorithme spécifié.
    
    - network : nom du fichier réseau pbf, sans l'extension
    - profile : nom du profil à utiliser, sans l'extension, ie car ou car_updated1
    - algorithm : algorithme du plus court chemin ie CH ou MLD 
    - pth_osrm_build : chemin d'accès vers le répertoire OSRM build contenant les fonctions de création du réseau
    - pth_osrm_profiles : chemin d'accès vers le répertoire contenant les profils OSRM
    - pth_folder_results : chemin d'accès vers le répertoire contenant les dossiers avec les fichiers du réseau obtenus en sortie
    - pth_results_network : chemin d'accès vers le répertoire contenant les fichiers du réseau obtenus en sortie
    """    
    try:
        os.chdir(pth_folder_results)

        cmd_extract = f'{pth_osrm_build}osrm-extract -p {pth_osrm_profiles}{profile}.lua {pth_results_network}{network}.osm.pbf --with-osm-metadata'
        os.system(cmd_extract)

        list_files = os.listdir(pth_folder_results)
        for file in list_files:
            if not file.endswith(('.pbf', '.ipynb', '.txt')):
                if not os.path.isdir(file):
                    shutil.move(f"{pth_folder_results}{file}", f"{pth_results_network}{file}") 

        if algorithm == "ch":
            cmd_contract = f'{pth_osrm_build}osrm-contract "{pth_results_network}{network}.osrm"'
            os.system(cmd_contract)

        elif algorithm == "mld":
            cmd_partition = f'{pth_osrm_build}osrm-partition {pth_results_network}{network}.osrm'
            os.system(cmd_partition)

            cmd_customize = f'{pth_osrm_build}osrm-customize {pth_results_network}{network}.osrm'
            os.system(cmd_customize)

        else:
            print("Entrer l'algorithme du plus court chemin 'MLD' ou 'CH' comme troisième argument")        

    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    construct_osrm(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
