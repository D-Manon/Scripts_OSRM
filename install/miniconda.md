# Guide d'installation miniconda

## 1. Télécharger l'installer
https://docs.conda.io/en/latest/miniconda.html#linux-installers (version Python 3.8)

## 2. Dans le terminal, exécuter :
bash Miniconda3-latest-Linux-x86_64.sh <br/>
cd Téléchargements/ <br/>
bash Miniconda3-py38_4.11.0-Linux-x86_64.sh 

## 3. Faire les configurations nécessaires puis, pour que les changements prennent effet, fermer et rouvrir le terminal

## 4. Création d'un nouvel environnement "stage"
conda create -n stage <br/>
conda activate stage

## 5. Installation des packages jupyterlab, pandas et altair
conda install -c conda-forge jupyterlab pandas altair
