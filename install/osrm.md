# Guide d'installation d'OSRM avec un Docker
---

## 1. Installation de Docker

```sudo apt update``` <br/> 
```sudo apt install apt-transport-https ca-certificates curl software-properties-common``` <br/>
```curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -``` <br/>
```sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"``` <br/>
```sudo apt update``` <br/>
On vérifie qu'on va installer le Docker à partir du dépôt Docker et non du dépôt Ubuntu par défaut <br/>
```apt-cache policy docker-ce``` <br/>
Installation de Docker <br/>
```sudo apt install docker-ce``` <br/>
On vérifie que le Docker tourne <br/>
```sudo systemctl status docker``` <br/>

## 2. Installation du backend d'OSRM en utilisant Docker
```sudo docker pull osrm/osrm-backend``` <br/>
```mkdir data``` <br/>
```cd data``` <br/>
```mkdir test``` <br/>
```cd test``` <br/>
Téléchargement d'un extrait du réseau OSM : le réseau des Hautes-Pyrénées <br/>
```sudo wget https://download.openstreetmap.fr/extracts/europe/france/midi_pyrenees/hautes_pyrenees.osm.pbf``` <br/>
```sudo docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/hautes_pyrenees-latest.osm.pbf``` <br/>
```sudo docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/hautes_pyrenees-latest.osrm``` <br/>
```sudo docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/hautes_pyrenees-latest.osrm``` <br/>
```sudo docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/hautes_pyrenees-latest.osrm```

## 3. Installation du frontend d'OSRM en utilisant Docker
```sudo docker pull osrm/osrm-frontend``` <br/>
```sudo docker run -p 9966:9966 osrm/osrm-frontend```
