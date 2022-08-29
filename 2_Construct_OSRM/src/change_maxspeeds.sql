--- Changement des maxspeeds d''OSM selon la méthodologie d'Odomatrix

--- Décomposition des tags sélectionnés (hstore) en colonnes (creation table temporaire)
CREATE TABLE tmp_table_tags_col AS 
SELECT *
FROM (
    SELECT
    id,
    tags -> 'name' as name,
    tags -> 'highway' as highway,
    tags -> 'incline' as incline,
    tags -> 'lanes' as lanes,
    tags -> 'junction' as junction,
    tags -> 'maxspeed' as maxspeed_osm,
    tags -> 'oneway' as oneway,
    tags -> 'smoothness' as smoothness,
    tags -> 'surface' as surface,
    tags -> 'traffic_calming' as traffic_calming,
    tags -> 'turn' as turn,
    tags -> 'width' as width,
    tags -> 'winter_road' as winter_road, 
    linestring
    FROM ways) as tags_cols;

--- Ajout de l'env_geo à la table temporaire créée
ALTER TABLE tmp_table_tags_col
Add column env_geo character varying,
Add column v_creuse smallint,
Add column v_pointe smallint,
Add column v_moyenne smallint;

UPDATE tmp_table_tags_col
SET env_geo = tmp_env_geo.env_geo_max
FROM tmp_env_geo
WHERE tmp_env_geo.id = tmp_table_tags_col.id;

--- Attribution des vitesses selon le type de route et d'environnement traversé
UPDATE tmp_table_tags_col
SET v_creuse = (
	case 
		
		when highway = 'residential' then 20
	
		when env_geo = '111MH' and highway = 'motorway' then 65
		when env_geo = '111MH' and highway = 'motorway_link' then 60
		when env_geo = '111MH' and highway = 'trunk' then 30
        when env_geo = '111MH' and highway = 'trunk_link' then 60
		when env_geo = '111MH' and highway = 'primary' then 30
        when env_geo = '111MH' and highway = 'primary_link' then 60
		when env_geo = '111MH' and highway = 'secondary' then 25
        when env_geo = '111MH' and highway = 'secondary_link' then 60
		when env_geo = '111MH' and highway = 'tertiary' then 20
        when env_geo = '111MH' and highway = 'tertiary_link' then 60
		when env_geo = '111MH' and highway = 'unclassified' then 20
		when env_geo = '111MH' and junction = 'roundabout' then 20
		
		when env_geo = '112MH' and highway = 'motorway' then 70
		when env_geo = '112MH' and highway = 'motorway_link' then 60
		when env_geo = '112MH' and highway = 'trunk' then 65
        when env_geo = '112MH' and highway = 'trunk_link' then 60
		when env_geo = '112MH' and highway = 'primary' then 30
        when env_geo = '112MH' and highway = 'primary_link' then 60
		when env_geo = '112MH' and highway = 'secondary' then 25
        when env_geo = '112MH' and highway = 'secondary_link' then 60
		when env_geo = '112MH' and highway = 'tertiary' then 20
        when env_geo = '112MH' and highway = 'tertiary_link' then 60
		when env_geo = '112MH' and highway = 'unclassified' then 20
		when env_geo = '112MH' and junction = 'roundabout' then 20
		
		when env_geo = '113MH' and highway = 'motorway' then 80
		when env_geo = '113MH' and highway = 'motorway_link' then 60
		when env_geo = '113MH' and highway = 'trunk' then 65
        when env_geo = '113MH' and highway = 'trunk_link' then 60
		when env_geo = '113MH' and highway = 'primary' then 30
        when env_geo = '113MH' and highway = 'primary_link' then 60
		when env_geo = '113MH' and highway = 'secondary' then 25
        when env_geo = '113MH' and highway = 'secondary_link' then 60
		when env_geo = '113MH' and highway = 'tertiary' then 20
        when env_geo = '113MH' and highway = 'tertiary_link' then 60
		when env_geo = '113MH' and highway = 'unclassified' then 20
		when env_geo = '113MH' and junction = 'roundabout' then 20
		
		when env_geo = '121MH' and highway = 'motorway' then 90
		when env_geo = '121MH' and highway = 'motorway_link' then 60
		when env_geo = '121MH' and highway = 'trunk' then 70
        when env_geo = '121MH' and highway = 'trunk_link' then 60
		when env_geo = '121MH' and highway = 'primary' then 40
        when env_geo = '121MH' and highway = 'primary_link' then 60
		when env_geo = '121MH' and highway = 'secondary' then 30
        when env_geo = '121MH' and highway = 'secondary_link' then 60
		when env_geo = '121MH' and highway = 'tertiary' then 20
        when env_geo = '121MH' and highway = 'tertiary_link' then 60
		when env_geo = '121MH' and highway = 'unclassified' then 20
		when env_geo = '121MH' and junction = 'roundabout' then 20

		when env_geo = '122MH' and highway = 'motorway' then 100
		when env_geo = '122MH' and highway = 'motorway_link' then 60
		when env_geo = '122MH' and highway = 'trunk' then 70
        when env_geo = '122MH' and highway = 'trunk_link' then 60
		when env_geo = '122MH' and highway = 'primary' then 40
        when env_geo = '122MH' and highway = 'primary_link' then 60
		when env_geo = '122MH' and highway = 'secondary' then 30
        when env_geo = '122MH' and highway = 'secondary_link' then 60
		when env_geo = '122MH' and highway = 'tertiary' then 20
        when env_geo = '122MH' and highway = 'tertiary_link' then 60
		when env_geo = '122MH' and highway = 'unclassified' then 20
		when env_geo = '122MH' and junction = 'roundabout' then 20
		
		when env_geo = '123MH' and highway = 'motorway' then 100
		when env_geo = '123MH' and highway = 'motorway_link' then 60
		when env_geo = '123MH' and highway = 'trunk' then 70
        when env_geo = '123MH' and highway = 'trunk_link' then 60
		when env_geo = '123MH' and highway = 'primary' then 40
        when env_geo = '123MH' and highway = 'primary_link' then 60
		when env_geo = '123MH' and highway = 'secondary' then 30
        when env_geo = '123MH' and highway = 'secondary_link' then 60
		when env_geo = '123MH' and highway = 'tertiary' then 20
        when env_geo = '123MH' and highway = 'tertiary_link' then 60
		when env_geo = '123MH' and highway = 'unclassified' then 20
		when env_geo = '123MH' and junction = 'roundabout' then 20
		
		when env_geo = '130MH' and highway = 'motorway' then 130
		when env_geo = '130MH' and highway = 'motorway_link' then 60
		when env_geo = '130MH' and highway = 'trunk' then 110
        when env_geo = '130MH' and highway = 'trunk_link' then 60
		when env_geo = '130MH' and highway = 'primary' then 85
        when env_geo = '130MH' and highway = 'primary_link' then 60
		when env_geo = '130MH' and highway = 'secondary' then 70
        when env_geo = '130MH' and highway = 'secondary_link' then 60
		when env_geo = '130MH' and highway = 'tertiary' then 40
        when env_geo = '130MH' and highway = 'tertiary_link' then 60
		when env_geo = '130MH' and highway = 'unclassified' then 40
		when env_geo = '130MH' and junction = 'roundabout' then 40
	
		when env_geo is NULL and highway = 'motorway' then 63
		when env_geo is NULL and highway = 'motorway_link' then 60
		when env_geo is NULL and highway = 'trunk' then 30
        when env_geo is NULL and highway = 'trunk_link' then 60
		when env_geo is NULL and highway = 'primary' then 30
        when env_geo is NULL and highway = 'primary_link' then 60
		when env_geo is NULL and highway = 'secondary' then 25
        when env_geo is NULL and highway = 'secondary_link' then 60
		when env_geo is NULL and highway = 'tertiary' then 20
        when env_geo is NULL and highway = 'tertiary_link' then 60
		when env_geo is NULL and highway = 'unclassified' then 40
		when env_geo is NULL and junction = 'roundabout' then 40
	END),
v_pointe = (	
	case 
	
		when highway = 'residential' then 20
	
		when env_geo = '111MH' and highway = 'motorway' then 35
		when env_geo = '111MH' and highway = 'motorway_link' then 42
		when env_geo = '111MH' and highway = 'trunk' then 16
        when env_geo = '111MH' and highway = 'trunk_link' then 42
		when env_geo = '111MH' and highway = 'primary' then 16
        when env_geo = '111MH' and highway = 'primary_link' then 42
		when env_geo = '111MH' and highway = 'secondary' then 14
        when env_geo = '111MH' and highway = 'secondary_link' then 42
		when env_geo = '111MH' and highway = 'tertiary' then 11
        when env_geo = '111MH' and highway = 'tertiary_link' then 42
		when env_geo = '111MH' and highway = 'unclassified' then 11
		when env_geo = '111MH' and junction = 'roundabout' then 11
		
		when env_geo = '112MH' and highway = 'motorway' then 41
		when env_geo = '112MH' and highway = 'motorway_link' then 47
		when env_geo = '112MH' and highway = 'trunk' then 41
        when env_geo = '112MH' and highway = 'trunk_link' then 47
		when env_geo = '112MH' and highway = 'primary' then 19
        when env_geo = '112MH' and highway = 'primary_link' then 47
		when env_geo = '112MH' and highway = 'secondary' then 16
        when env_geo = '112MH' and highway = 'secondary_link' then 47
		when env_geo = '112MH' and highway = 'tertiary' then 13
        when env_geo = '112MH' and highway = 'tertiary_link' then 47
		when env_geo = '112MH' and highway = 'unclassified' then 13
		when env_geo = '112MH' and junction = 'roundabout' then 13
		
		when env_geo = '113MH' and highway = 'motorway' then 70
		when env_geo = '113MH' and highway = 'motorway_link' then 54
		when env_geo = '113MH' and highway = 'trunk' then 53
        when env_geo = '113MH' and highway = 'trunk_link' then 54
		when env_geo = '113MH' and highway = 'primary' then 25
        when env_geo = '113MH' and highway = 'primary_link' then 54
		when env_geo = '113MH' and highway = 'secondary' then 20
        when env_geo = '113MH' and highway = 'secondary_link' then 54
		when env_geo = '113MH' and highway = 'tertiary' then 16
        when env_geo = '113MH' and highway = 'tertiary_link' then 54
		when env_geo = '113MH' and highway = 'unclassified' then 16
		when env_geo = '113MH' and junction = 'roundabout' then 16
		
		when env_geo = '121MH' and highway = 'motorway' then 70
		when env_geo = '121MH' and highway = 'motorway_link' then 42
		when env_geo = '121MH' and highway = 'trunk' then 53
        when env_geo = '121MH' and highway = 'trunk_link' then 42
		when env_geo = '121MH' and highway = 'primary' then 28
        when env_geo = '121MH' and highway = 'primary_link' then 42
		when env_geo = '121MH' and highway = 'secondary' then 19
        when env_geo = '121MH' and highway = 'secondary_link' then 42
		when env_geo = '121MH' and highway = 'tertiary' then 12
        when env_geo = '121MH' and highway = 'tertiary_link' then 42
		when env_geo = '121MH' and highway = 'unclassified' then 12
		when env_geo = '121MH' and junction = 'roundabout' then 12

		when env_geo = '122MH' and highway = 'motorway' then 60
		when env_geo = '122MH' and highway = 'motorway_link' then 47
		when env_geo = '122MH' and highway = 'trunk' then 57
        when env_geo = '122MH' and highway = 'trunk_link' then 47
		when env_geo = '122MH' and highway = 'primary' then 31
        when env_geo = '122MH' and highway = 'primary_link' then 47
		when env_geo = '122MH' and highway = 'secondary' then 21
        when env_geo = '122MH' and highway = 'secondary_link' then 47
		when env_geo = '122MH' and highway = 'tertiary' then 13
        when env_geo = '122MH' and highway = 'tertiary_link' then 47
		when env_geo = '122MH' and highway = 'unclassified' then 13
		when env_geo = '122MH' and junction = 'roundabout' then 13
		
		when env_geo = '123MH' and highway = 'motorway' then 100
		when env_geo = '123MH' and highway = 'motorway_link' then 54
		when env_geo = '123MH' and highway = 'trunk' then 64
        when env_geo = '123MH' and highway = 'trunk_link' then 54
		when env_geo = '123MH' and highway = 'primary' then 36
        when env_geo = '123MH' and highway = 'primary_link' then 54
		when env_geo = '123MH' and highway = 'secondary' then 26
        when env_geo = '123MH' and highway = 'secondary_link' then 54
		when env_geo = '123MH' and highway = 'tertiary' then 17
        when env_geo = '123MH' and highway = 'tertiary_link' then 54
		when env_geo = '123MH' and highway = 'unclassified' then 17
		when env_geo = '123MH' and junction = 'roundabout' then 17
		
		when env_geo = '130MH' and highway = 'motorway' then 130
		when env_geo = '130MH' and highway = 'motorway_link' then 60
		when env_geo = '130MH' and highway = 'trunk' then 110
        when env_geo = '130MH' and highway = 'trunk_link' then 60
		when env_geo = '130MH' and highway = 'primary' then 85
        when env_geo = '130MH' and highway = 'primary_link' then 60
		when env_geo = '130MH' and highway = 'secondary' then 70
        when env_geo = '130MH' and highway = 'secondary_link' then 60
		when env_geo = '130MH' and highway = 'tertiary' then 40
        when env_geo = '130MH' and highway = 'tertiary_link' then 60
		when env_geo = '130MH' and highway = 'unclassified' then 40
		when env_geo = '130MH' and junction = 'roundabout' then 40
	
		when env_geo is NULL and highway = 'motorway' then 35
		when env_geo is NULL and highway = 'motorway_link' then 42
		when env_geo is NULL and highway = 'trunk' then 16
        when env_geo is NULL and highway = 'trunk_link' then 42
		when env_geo is NULL and highway = 'primary' then 16
        when env_geo is NULL and highway = 'primary_link' then 42
		when env_geo is NULL and highway = 'secondary' then 14
        when env_geo is NULL and highway = 'secondary_link' then 42
		when env_geo is NULL and highway = 'tertiary' then 11
        when env_geo is NULL and highway = 'tertiary_link' then 42
		when env_geo is NULL and highway = 'unclassified' then 40
		when env_geo is NULL and junction = 'roundabout' then 40
	
	END);

UPDATE tmp_table_tags_col
SET v_moyenne = (v_creuse + v_pointe)/2;

--- Suppression des maxspeed_osm mal remplis
ALTER TABLE tmp_table_tags_col
Add column isnumeric boolean;

UPDATE tmp_table_tags_col
SET isnumeric = textregexeq(maxspeed_osm,'^[[:digit:]]+(\.[[:digit:]]+)?$');

UPDATE tmp_table_tags_col
SET maxspeed_osm = (
	case
		when isnumeric = 'true' then maxspeed_osm
        else NULL
    end);

ALTER TABLE tmp_table_tags_col
ALTER COLUMN maxspeed_osm TYPE smallint USING maxspeed_osm::smallint;

-- Conservation du maxspeed lorsqu'il est inférieur aux vitesses en heures creuse, pointe et moyenne
UPDATE tmp_table_tags_col
SET v_creuse = (
    case
        when maxspeed_osm < v_creuse then maxspeed_osm
        else v_creuse
    END),
    v_pointe = (
    case
        when maxspeed_osm < v_pointe then maxspeed_osm
        else v_pointe 
    END),
    v_moyenne = (
    case
        when maxspeed_osm < v_moyenne then maxspeed_osm
        else v_moyenne 
    END);

---UPDATE tmp_table_tags_col
---SET v_choisie = (
---    case
---        when env_geo = '111MH' then v_moyenne
---		when env_geo = '121MH' then v_moyenne
---       else v_creuse
---    END);
    
-- Conversion des vitesses en text (format osm)
ALTER TABLE tmp_table_tags_col ALTER COLUMN v_creuse TYPE text USING v_creuse::text;
ALTER TABLE tmp_table_tags_col ALTER COLUMN v_pointe TYPE text USING v_pointe::text;
ALTER TABLE tmp_table_tags_col ALTER COLUMN v_moyenne TYPE text USING v_moyenne::text;
---ALTER TABLE tmp_table_tags_col ALTER COLUMN v_choisie TYPE text USING v_choisie::text;
ALTER TABLE tmp_table_tags_col ALTER COLUMN maxspeed_osm TYPE text USING maxspeed_osm::text;


--- Recomposition de la colonne tags au format hstore
create table tmp_table_tags_hstore as
select * , hstore(ARRAY[
    ['name',name],
    ['highway',highway],
    ['incline',incline],
    ['lanes',lanes],
    ['junction',junction],
    ['maxspeed',v_moyenne], 
    ['oneway',oneway],
    ['smoothness',smoothness],
    ['surface',surface],
    ['traffic_calming',traffic_calming],
    ['turn',turn],
    ['width',width],
    ['winter_road',winter_road]
]) as tags
from tmp_table_tags_col;

--- Suppression des tags NULL 
UPDATE tmp_table_tags_hstore
SET tags=subquery.tags
FROM (SELECT id, tags::hstore - '"name"=>NULL, "highway"=>NULL, "incline"=>NULL, "lanes"=>NULL, "junction"=>NULL, "maxspeed"=>NULL, "oneway"=>NULL, "smoothness"=>NULL, "surface"=>NULL, "traffic_calming"=>NULL, "turn"=>NULL, "width"=>NULL, "winter_road"=>NULL'::hstore as tags
    FROM tmp_table_tags_hstore) AS subquery
WHERE tmp_table_tags_hstore.id=subquery.id;

--- Modification vitesse
--UPDATE tmp_table_tags_hstore
--SET tags = tags || hstore('maxspeed', '200')

--- Modification des tags de ways (importation des changements)
UPDATE ways
SET tags = tmp_table_tags_hstore.tags
FROM tmp_table_tags_hstore
WHERE tmp_table_tags_hstore.id = ways.id;
