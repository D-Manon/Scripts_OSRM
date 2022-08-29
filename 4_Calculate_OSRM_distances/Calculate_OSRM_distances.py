'''
A partir d'un fichier csv avec des coordonnées, calcule les distances entre des paires de lieux avec le calculateur d'itinéraires OSRM.
- data : nom du fichier csv, sans l'extension
- format_line : indiquer si une ligne correspond à un seul lieu ('lieu') ou à un couple de lieux ('trajet')
'''

import os
import sys
from pathlib import Path
import requests
import pandas as pd
import itertools as it
from datetime import datetime

os.chdir(Path(__file__).parent)
print(os.getcwd())
start = datetime.now()

data = sys.argv[1]
format_line = sys.argv[2]

table = pd.read_csv(f'./Data/{data}.csv')

if format_line == "trajet":
# Inversion de l'ordre des coordonnées : longitude,latitude plutôt que latitute,longitude (ordre dans la requête à OSRM)
    table["O"] = table["O_lon"].apply(str) + "," + table["O_lat"].apply(str)
    table["D"] = table["D_lon"].apply(str) + "," + table["D_lat"].apply(str)
    list_coord = list(zip(table.O, table.D)) # Liste des paires de coordonnées des trajets
elif format_line == "lieu":
## Permutation si une ligne = un lieu
    table["coord"] = table["lon"].apply(str) + "," + table["lat"].apply(str)
    table_couples = it.permutations(list(table['coord']), 2)
    list_coord = list(table_couples)    
else:
    print("Veuillez indiquer si une ligne du fichier csv correspond à un seul lieu ('lieu') ou à un couple de lieux ('trajet')")



def calcul_distances() :
    ''' Calcule des distances entre des couples de coordonnées 
    '''
    list_ntest = []
    list_depart = []
    list_arrivee = []
    list_distance = []                     
    list_duration = []

    
    for i in range(len(list_coord)):
        O = list_coord[i][0]
        D = list_coord[i][1]
    
        params = {
            'overview': 'false',
        }

        r = requests.get(url=f'http://localhost:5000/route/v1/driving/{O};{D}', params=params)
        distance = r.json()['routes'][0]['distance'] / 1000
        duration = r.json()['routes'][0]['duration'] / 60

        list_ntest.append(i+1)
        list_depart.append(O)
        list_arrivee.append(D)
        list_distance.append(distance)
        list_duration.append(duration)
    
    distance_table = { 
        'Test' : list_ntest,
        'Départ' : list_depart,
        'Arrivée' : list_arrivee,
    }
    
    distance_table[f'Distance OSRM'] = list_distance
    distance_table[f'Durée OSRM'] = list_duration
    
    distance_table = pd.DataFrame(distance_table)
    distance_table.to_csv(f'./Results/dist_{data}.csv', index=False)

    
    
def main():
    try:
        calcul_distances(sys.argv[3])
        end = datetime.now()
        print(end-start)
        
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main()
