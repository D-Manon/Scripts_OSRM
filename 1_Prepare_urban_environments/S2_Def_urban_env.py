'''
Ce script permet d'attribuer un type d'environnement urbain à chaque morceau de commune (= intersection CLC et commune) selon le code CLC, la population de la commune et la population de l'aire d'attraction dans laquelle le morceau s'inscrit.
'''

from datetime import datetime
from env import EnvVar
import geopandas as gpd
import os

os.chdir('/home/manon/Documents/Scripts_OSRM/1_Prepare_urban_environments/')

def get_env(df):
    if df["POPPUZAU"] < 200000 and df["CATEAAV2020"] == '20' and df["CODE_CLC"] == '122' : # on élimine les autoroutes
        ENV_GEO = "130MH"
    elif (df["POPULATION"] > 50000 and (
            df["CATEAAV2020"] == '11' or df["CATEAAV2020"] == '12' or df["CATEAAV2020"] == '13') and df[
              "POPPUZAU"] > 200000 and (df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "111MH"
    elif (df["POPULATION"] > 50000 and (
            df["CATEAAV2020"] == '11' or df["CATEAAV2020"] == '12' or df["CATEAAV2020"] == '13') and 100000 <= df[
              "POPPUZAU"] <= 200000 and (df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "112MH"
    elif (df["POPULATION"] > 50000 and (
            df["CATEAAV2020"] == '11' or df["CATEAAV2020"] == '12' or df["CATEAAV2020"] == '13') and df[
              "POPPUZAU"] < 100000 and (df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "113MH"
    elif (df["POPULATION"] < 50000 and (
            df["CATEAAV2020"] == '11' or df["CATEAAV2020"] == '12' or df["CATEAAV2020"] == '13' or df[
        "CATEAAV2020"] == '20') and df["POPPUZAU"] > 200000 and (
                  df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "121MH"
    elif (df["POPULATION"] < 50000 and (
            df["CATEAAV2020"] == '11' or df["CATEAAV2020"] == '12' or df["CATEAAV2020"] == '13' or df[
        "CATEAAV2020"] == '20') and 100000 <= df["POPPUZAU"] <= 200000 and (
                  df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "122MH"
    elif (df["POPULATION"] < 50000 and (
            df["CATEAAV2020"] == '11' or df["CATEAAV2020"] == '12' or df["CATEAAV2020"] == '13' or df[
        "CATEAAV2020"] == '20') and df["POPPUZAU"] < 100000 and (
                  df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "123MH"
    elif ((df["CATEAAV2020"] == '20' or df["CATEAAV2020"] == '30') and (
            df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511')):
        ENV_GEO = "130MH"
    elif not (df["CODE_CLC"].startswith('1') or df["CODE_CLC"] == '511'):
        ENV_GEO = "130MH"
    else:
        ENV_GEO = 'PB'
    return ENV_GEO


def main():
    try:
        start = datetime.now()
        pth_folder_data = EnvVar.paths['pth_folder_data']
        df_com_zau_clc = gpd.read_file("./Data/com_zau.gpkg") # mettre chemin d'accès correspondant
        df_com_zau_clc['env_geo'] = df_com_zau_clc.apply(get_env, axis=1)
        df_com_zau_clc = df_com_zau_clc.set_crs("EPSG:3857", allow_override=True)
        df_com_zau_clc = df_com_zau_clc.to_crs("EPSG:4326")
        df_com_zau_clc.to_file(f"{pth_folder_data}env_geo_updated.gpkg", layer='env_geo_updated', driver="GPKG")
        end = datetime.now()
        print(f"Temps d'exécution préparation des environnements urbains : {end-start} ")
    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    main()
