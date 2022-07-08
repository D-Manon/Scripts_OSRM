import os
import shutil
import sys

def run_osrm(network, profile, algorithm) :
    os.chdir('/home/manon/Documents/BDD/OSM')
    path_data_folder = os.getcwd() + '/'
    algorithm = algorithm.lower()
    path_data = f"{path_data_folder}{network}/{profile}/{algorithm}/"
    
    if algorithm == "ch":
        cmd_routed = f'osrm-routed {path_data}{network}_with_geom.osrm'
        os.system(cmd_routed)
        
    elif algorithm == "mld":
        cmd_routed = f'osrm-routed --algorithm=MLD {path_data}{network}_with_geom.osrm'
        os.system(cmd_routed)
        
    else:
        print("Entrer l'algorithme du plus court chemin 'MLD' ou 'CH' comme troisième argument")
        
def main():
    try:
        run_osrm(sys.argv[1], sys.argv[2], sys.argv[3])
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main()
