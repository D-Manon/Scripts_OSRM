from dotenv import load_dotenv
from os import environ, path
from pathlib import Path


class EnvVar:
    BASE_DIR = Path(__file__).parent.parent
    load_dotenv(path.join(BASE_DIR, "../.env"), verbose=True)
    
    options = dict(
        env_geo = environ.get('env_geo'),
        network = environ.get('network'),
        url_network = environ.get('url_network'),
        algorithm = environ.get('algorithm'),
        profile = environ.get('profile'))

    connexion_pg = dict(
        db_superuser = environ.get('db_superuser'),
        db_superpassword = environ.get('db_superpassword'),
        db_superdb = environ.get('db_superdb'),
        db_user = environ.get('db_user'),
        db_host = environ.get('db_host'),
        db_port = environ.get('db_port'),
        db_name = environ.get('db_name'),
        db_password = environ.get('db_password'))

    paths = dict(
        pth_main_folder=environ.get('pth_main_folder'),
        pth_scripts=environ.get('pth_scripts'),
        pth_folder_data=environ.get('pth_folder_data'),
        pth_folder_results=environ.get('pth_folder_results'),
        pth_results_network=environ.get('pth_results_network'),
        pth_folder_osmosis=environ.get('pth_folder_osmosis'),
        pth_osmosis_scripts=environ.get('pth_osmosis_scripts'),
        pth_osmosis=environ.get('pth_osmosis'),
        pth_folder_osrm=environ.get('pth_folder_osrm'),
        pth_osrm_build=environ.get('pth_osrm_build'),
        pth_osrm_profiles=environ.get('pth_osrm_profiles'))
    
