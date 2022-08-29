# Scripts_OSRM

Cet ensemble de dossiers et de scripts permet de mettre en place un **calculateur d’itinéraires fonctionnant avec OSRM** et dont les vitesses sont configurées de manière à prendre en compte **l’environnement urbain traversé** par les tronçons de route. Cette prise en compte de l’environnement urbain s’appuie sur la méthodologie développée par l’unité CESAER de l’INRA Dijon pour le logiciel Odomatrix. Il s’agit de prendre en considération les ralentissements aux abords des zones urbaines très denses dus à l’important flux de circulation.

Mohamed Hilal. ODOMATRIX. Calcul de distances routières intercommunales. Cahier des Techniques de l'INRA, INRA, 2010, pp.41-63. ⟨hal-02666703⟩ 

Avant de lancer les scripts, il faut au préalable avoir téléchargé le **back-end d’OSRM**. Mise en place détaillée ici : install/osrm.md 
[https://github.com/D-Manon/Scripts_OSRM/blob/71cf2a593470b13fb3be2c8dc8165775eacf2f44/install/osrm.md]


Les dossiers listés ci-dessous contiennent un ou plusieurs scripts python permettant de réaliser les opérations suivantes :
- **1_Prepare_urban_environments** : Définition de types d’environnements urbains à partir des données INSEE et du Corine Land Cover (méthodologie basée sur celle appliquée par l’INRA Dijon). En sortie de ce script, on obtient un fichier vectoriel au format gpkg.
- **2_Construst_OSRM** : Construction du calculateur d’itinéraires OSRM prenant en compte les environnements urbains définis précédemment, traversés par les tronçons de route. En sortie, on obtient tous les fichiers nécessaires au lancement d’OSRM.
- **3_Run_OSRM** : Mise en route du serveur OSRM
- **4_Calculate_distances_OSRM** : Calcul automatisé de plusieurs distances avec le serveur OSRM mis en route à partir d’un fichier csv comprenant des coordonnées. En sortie, on obtient un fichier csv avec tous les temps de trajet calculés.

Rq :
Le fichier *env* est à renommer en *.env*  
Il rassemble les variables nécessaires au fonctionnement des scripts. Celles-ci peuvent être modifiées pour ajuster les chemins d'accès et pour configurer les paramètres souhaités.

## 1 - Préparation des environnements urbain (1_Prepare_urban_environments)
Scripts de ce dossier initialement écrits par Florian Bayer, modifiés par Manon Despaux

Voir aussi data/environnement/

Trois étapes successives : 
1) Jointure de la population INSEE, des aires d’attraction INSEE, des géométries des communes → Lancer **S1_Prepa_data_com.ipynb**
2) Intersection du fichier gpkg obtenu avec le CLC : **étape à réaliser sur QGIS ou ArcGIS**
wget [ftp://Corine_Land_Cover_ext:ishiteimapie9ahP@ftp3.ign.fr/ftp://Corine_Land_Cover_ext:ishiteimapie9ahP@ftp3.ign.fr/CLC18_SHP__FRA_2019-08-21.7z]
3) Attribution d’un type d’environnement urbain à chaque morceau de commune (un morceau de commune = intersection CLC et de la commune) → Lancer **S2_Dep_urban_env.py** `python3 /home/manon/Documents/Scripts/1_Prepare_urban_environments/ S2_Dep_urban_env.py`

En sortie : *env_geo_updated.gpkg* → fichier vectoriel contenant les environnements urbains à l’échelle de la France entière

Le dossier comprend aussi les éléments suivants :
- Data/ : dossier contenant les données téléchargées grâce au script S1 + les données CLC 2020 à utiliser pour l’étape 2
- env.py : classe EnvVar définissant et appelant les valeurs des paramètres et variables des différents scripts depuis le fichier .env présent à la racine. Cela permet de centraliser la définition des variables.


## 2 - Construction du calculateur d’itinéraires avec OSRM (2_Construst_OSRM)
Lancer la commande `python3 /home/manon/Documents/Scripts/2_Construct_OSRM/Construction_OSRM_AZ.py`

Le dossier comprend les éléments suivants :
- **Construction_OSRM_AZ.py** : script principal lançant des instructions dans l’invite de commandes ainsi que des fonctions contenues dans des scripts python présents dans le dossier src.
- src/ : scripts appelés et lancés par le script principal, numérotés de 1 à 3
  + env.py : classe EnvVar définissant et appelant les valeurs des paramètres et variables des différents scripts depuis le fichier .env présent à la racine. Cela permet de centraliser la définition des variables.
  + utils.py : classe Timer avec méthodes permettant de démarrer un compteur et de l’arrêter en enregistrant la durée calculée dans un document texte.
  + **S1_Creation_BDD.py** : définit la fonction create_db qui permet la création de la base de données postgresql avec les extensions nécessaires (hstore et postgis).
  + **S2_Configuration_vitesses.py** : change_maxspeeds permet d’attribuer un environnement urbain à chaque tronçon OSM et une vitesse définie en conséquence. Le type d’environnement attribué est celui que le tronçon parcourt le plus au total. Pour ce faire, le script SQL change_maxspeeds.sql présent dans le même dossier est lancé. 
          En entrée : le fichier pbf à modifier (stocké dans assets)
          En sortie : le fichier pbf modifié (stocké dans results)
  + **S3_Construction_OSRM.py** : le réseau est construit à partir des données OSM précédemment modifiées et selon l’algorithme spécifié (MLD ou CH)
    + En entrée : le fichier pbf modifié (stocké dans results), le profil lua (car_updated1 dans notre cas, stocké dans assets mais en réalité dans le dossier dédié à OSRM créé lors de son installation)
    + En sortie : tous les fichiers nécessaires au lancement du serveur OSRM. Ils sont stockés dans le dossier results
- assets/ : les données en entrée env_geo_updated.gpkg et le fichier pbf initial (téléchargé dans le script si non présent)
- results/ : dossier stockant les fichier obtenus en sortie  




Entrées : 
- Le fichier vectoriel des environnements urbains (*env_geo_updated.gpkg*)
- Un jeu de données OSM (dont le téléchargement est lancé dans le script si besoin)

Sortie intermédiaire : données OSM modifiées (modification maxspeed)

Sorties :
- Tous les fichiers nécessaires au fonctionnement d’OSRM (dans results/)
- Document texte recensant le temps d’exécution des différentes étapes (dans results/)

## 3 - Mise en route d’OSRM (3_Run_OSRM)
Lancer la commande `python3 ./Scripts/3_Run_OSRM/Run_OSRM.py`

Le script met en route le back-end d’OSRM. 
Paramètres du script :
- *network* : nom du fichier réseau pbf, sans l'extension
- *profile* : nom du profil à utiliser, sans l'extension, c’est-à-dire car, foot, bicycle ou car_updated1
- *algorithm* : algorithme du plus court chemin c’est-à-dire CH ou MLD

## 4 - Calcul de distances (4_Calculate_OSRM_distances)
Calculate_OSRM_distances : à partir d'un fichier csv avec des coordonnées, calcule les distances (en kilomètres et en minutes) entre des paires de lieux avec le calculateur d’itinéraires OSRM.
Paramètres du script : 
- *data* : nom du fichier csv, sans l'extension
- *format_line* : indiquer si une ligne correspond à un seul lieu ('lieu') ou à un couple de lieux ('trajet')


