# Guide d'installation d'OSRM
---

## 1. Installation de Docker

```
sudo apt update

sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

sudo apt update
```

On vérifie qu'on va installer le Docker à partir du dépôt Docker et non du dépôt Ubuntu par défaut <br/>
```apt-cache policy docker-ce``` <br/>

Installation de Docker <br/>
```sudo apt install docker-ce``` <br/>

On vérifie que le Docker tourne <br/>
```sudo systemctl status docker``` <br/>

## 2. Installation du backend d'OSRM en utilisant Docker
```
sudo docker pull osrm/osrm-backend

mkdir data

cd data

mkdir test

cd test
```
Téléchargement d'un extrait du réseau OSM : le réseau des Hautes-Pyrénées <br/>
```
sudo wget https://download.openstreetmap.fr/extracts/europe/france/midi_pyrenees/hautes_pyrenees.osm.pbf

sudo docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/hautes_pyrenees-latest.osm.pbf

sudo docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/hautes_pyrenees-latest.osrm

sudo docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/hautes_pyrenees-latest.osrm

sudo docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/hautes_pyrenees-latest.osrm
```

## 3. Installation du backend d'OSRM sans Docker
```
sudo apt update

sudo apt install build-essential git cmake pkg-config doxygen libboost-all-dev libtbb-dev lua5.2 liblua5.2-dev libluabind-dev libstxxl-dev libstxxl1v5 libxml2 libxml2-dev libosmpbf-dev libbz2-dev libzip-dev libprotobuf-de

sudo useradd -d /srv/osrm -s /bin/bash -m osrm

sudo apt install acl

sudo setfacl -R -m u:manon:rwx /srv/osrm/

cd /srv/osrm/

git clone https://github.com/Project-OSRM/osrm-backend.git

mkdir build

cd build

cmake /srv/osrm/osrm-backend/

make

sudo make install
```

Installation de GNU Screen
```
sudo apt install screen

screen
```

Téléchargement d'un extrait du réseau OSM : le réseau des Hautes-Pyrénées 
```
sudo wget https://download.openstreetmap.fr/extracts/europe/france/midi_pyrenees/hautes_pyrenees.osm.pbf

cd /srv/osrm/osrm-backend/

osrm-extract hautes_pyrenees-latest.osm.pbf --threads=10

osrm-partition hautes_pyrenees-latest.osrm

osrm-customize hautes_pyrenees-latest.osrm
```

Lancer OSRM
```
osrm-routed --algorithm=MLD hautes_pyrenees-latest.osrm
```

## 4. Installation du frontend d'OSRM en utilisant Docker
```
sudo docker pull osrm/osrm-frontend

sudo docker run -p 9966:9966 osrm/osrm-frontend
```
