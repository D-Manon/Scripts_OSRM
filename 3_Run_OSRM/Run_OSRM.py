"""
Met en route le calculateur d'itinéraires
- network : nom du fichier réseau pbf, sans l'extension
- algorithm : algorithme du plus court chemin ie CH ou MLD
"""

import os
from env import EnvVar


def run_osrm(network, algorithm):
    pth_results_network = EnvVar.paths['pth_results_network']
    
    if algorithm == "ch":
        cmd_routed = f'osrm-routed {pth_results_network}{network}_updated.osrm'
        os.system(cmd_routed)
        
    elif algorithm == "mld":
        cmd_routed = f'osrm-routed --algorithm=MLD {pth_results_network}{network}_updated.osrm'
        os.system(cmd_routed)
        
    else:
        print("Entrer l'algorithme du plus court chemin 'MLD' ou 'CH' comme troisième argument")


def main():
    try:
        network = EnvVar.options['network']
        algorithm = EnvVar.options['algorithm'].lower()
        run_osrm(network, algorithm)
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main()
