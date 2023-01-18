import os
import sys
from itertools import combinations
import psycopg2
from sqlalchemy import create_engine
import pandas.io.sql as psql

sys.path.insert(0, "/home/manon/Documents/Scripts/src")
from src.env import EnvVar


def add_airways(db_name, db_password, pth_folder_data):
    """
    Commentaire
    """

    try:
        db_host = EnvVar.connexion_pg['db_host']
        db_port = EnvVar.connexion_pg['db_port']
        db_user = EnvVar.connexion_pg['db_user']

        # 1. Import fichier aeroports dans bdd postgresql
        cmd_import_gpkg_postgis = f"ogr2ogr -f PostgreSQL PG:\"dbname={db_name} host={db_host} port={db_port} user={db_user} password={db_password}\" {pth_folder_data}transport.gpkg na_aeroport_ABM"
        os.system(cmd_import_gpkg_postgis)

        # 2. Formatage table aeroport puis integration a table nodes
        # Connexion bdd
        con = psycopg2.connect(dbname=db_name, user=db_user, host=db_host, password=db_password)
        cur = con.cursor()

        cur.execute("""
        INSERT INTO users VALUES (20222023, 'Manon');

        ALTER TABLE na_aeroport_abm
        Add column geom geometry,
        Add column version integer, 
        Add column user_id integer, 
        Add column tstamp timestamp, 
        Add column changeset_id bigint,
        Add column tags hstore;

        create sequence if not exists public.nodes_id_sequence ;
        select setval('nodes_id_sequence', (select max(id)+1 from nodes)) ;

        create sequence if not exists public.ways_id_sequence ;
        select setval('ways_id_sequence', (select max(id)+1 from ways)) ;

        UPDATE na_aeroport_abm
        SET 
        id = nextval('nodes_id_sequence'),
        geom = st_transform(ST_Force2D("Shape"), 4326),
        version = 1,
        user_id = 20222023,
        tstamp = '2023-01-11 12:30:00',
        changeset_id = 202220233,
        tags = hstore(ARRAY[
            ['name',nom],
            ['highway','airport']]);

        ALTER TABLE na_aeroport_abm ALTER COLUMN id TYPE bigint USING id::bigint;

        INSERT INTO nodes (id, geom, version, user_id, tstamp, changeset_id)
        select id, geom, version, user_id, tstamp, changeset_id from na_aeroport_abm;""")
        con.commit()

        # 3. Creation des paires d'aeroports
        # Connexion bdd avec autre outil
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        c = engine.connect()
        conn = c.connection
        df_aero_pg = psql.read_sql("SELECT * FROM na_aeroport_abm", con=conn)
        trajets_aero = [list(comb) for comb in combinations(list(df_aero_pg['id']), 2)]

        # 4. Creation des airways
        for i in range(len(trajets_aero)):
            cur.execute("""INSERT INTO ways (id, version, user_id, tstamp, changeset_id, tags, nodes, linestring)
             VALUES
             (nextval('ways_id_sequence'), 1, 20222023, (SELECT '2023-01-11 16:00:00'::TIMESTAMP), 202220233, '"name"=>"test1","highway"=>"airway","maxspeed"=>"300"', '{%(O)s,%(D)s}', (select ST_MakeLine(geom) from nodes where id in (%(O)s,%(D)s)));
            """, {'O': trajets_aero[i][0], 'D': trajets_aero[i][1]})

            cur.execute("""INSERT INTO way_nodes (way_id, node_id, sequence_id)
                         VALUES 
                         (lastval(), %(O)s, 0),
                         (lastval(), %(D)s, 1);
            """, {'O': trajets_aero[i][0], 'D': trajets_aero[i][1]})
        con.commit()

        # 5. Selection des nodes dans buffer de 1000m
        for i in range(len(df_aero_pg)):
            node_proche_id = psql.read_sql(f"""
                                            select id 
                                            from (
                                                select id, geom,  ST_Distance('{df_aero_pg['geom'][i]}'::geography, geom::geography) dist from (select * from nodes where id not between 10537925776 and 110537925876) as nodes
                                                where st_dwithin('{df_aero_pg['geom'][i]}'::geography, geom::geography, 1000) is true
                                                order by dist asc
                                            ) as nodes_1km
                                            limit 1
                                           """, con=conn)

            cur.execute("""
            INSERT INTO ways (id, version, user_id, tstamp, changeset_id, tags, nodes, linestring)
            VALUES (nextval('ways_id_sequence'), 1, 20222023, (SELECT '2023-01-13 17:16:00'::TIMESTAMP), 202220233, '"name"=>"lien_aeroport","highway"=>"primary","maxspeed"=>"20"', '{%(node_proche_id)s,%(aero_id)s}', (select ST_MakeLine(geom) from nodes where id in (%(node_proche_id)s,%(aero_id)s)));""",
                        {'node_proche_id': node_proche_id.iloc[0, 0].item(), 'aero_id': df_aero_pg['id'][i].item()})
            con.commit()

            cur.execute("""INSERT INTO way_nodes (way_id, node_id, sequence_id)
                     VALUES 
                     (lastval(), %(O)s, 0),
                     (lastval(), %(D)s, 1);
        """, {'O': node_proche_id.iloc[0, 0].item(), 'D': df_aero_pg['id'][i].item()})
            con.commit()

        conn.close()
        con.close()


    except Exception as exception:
        print(f"{type(exception).__name__} at line {exception.__traceback__.tb_lineno} of {__file__}: {exception}")


if __name__ == "__main__":
    add_airways(sys.argv[1], sys.argv[2], sys.argv[3])
