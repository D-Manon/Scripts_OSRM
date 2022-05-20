# Création des entités géographiques afin de définir le type d'environnement. L'environnement traversé par les routes est drappé sur les tronçons de route pour pondérer la vitesse

1. import des aires urbaines de l'INSEE
2. Jointure avec la géométrie des communes (doit contenir la population de la commune)
3. Intersect du résultat précédent avec CLC (à faire dans Qgis pour des questions de performance)
