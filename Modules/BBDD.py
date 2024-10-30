
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import mysql
import mysql.connector



#Creacion database y tablas

def creacion_database(database):
    try:

        db = mysql.connector.connect(host     = "localhost",
                                    user     = "root",
                                    password = "password",
                                    database = None)

        db.autocommit = True  # Aseguramos que los cambios se confirmen automáticamente
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};") #crear database

        cursor.close()
        db.close()

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database=database
            )
        cursor = db.cursor()


        query_artist = f"""CREATE TABLE IF NOT EXISTS artistas (
            artista_id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );"""


        cursor.execute(query_artist)
        print("Tabla 'artistas' creada o ya existía.") 


        query_canciones = f"""CREATE TABLE IF NOT EXISTS canciones (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            artista_id INT REFERENCES artistas(artista_id),
            duracion_segundos FLOAT,
            popularidad INT,
            explicito BOOLEAN,
            fecha_lanzamiento DATE,
            danceability FLOAT,
            energy FLOAT,
            valence FLOAT,
            tempo FLOAT,
            acousticness FLOAT,
            instrumentalness FLOAT,
            speechiness FLOAT,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );"""

        cursor.execute(query_canciones)
        print("Tabla 'canciones' creada o ya existía.")
    except Error as e:
            print(f"Error al crear la base de datos o las tablas: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



# Carga en tablas


def load_data(df):
    user = 'root'
    password = 'password'
    database = 'Proyecto_Spotify'
    host = "localhost"
    port = 3306

    # Crear la conexión
    try:
        engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost/{database}')

        # Abrir la conexión
        connection = engine.connect()

        artistas_df = df[['Artistas']].drop_duplicates().rename(columns = {'Artistas': 'nombre'})
        artistas_df.to_sql('artistas', con = engine, if_exists = 'append', index = False)
        
        # Obtener los ID de los artistas.
        with engine.connect() as connection:
            artistas_db_df = pd.read_sql('SELECT * FROM artistas', connection)

        # Fusionar DF para obtener el 'artista_id' correspondiente.
        df_merged = df.merge(artistas_db_df, left_on = 'Artistas', right_on = 'nombre', how = 'left')

        # Eliminar 'nombre' de estar duplicado.
        if 'nombre' in df_merged.columns:
            df_merged = df_merged.drop(columns=['nombre'])

        # Renombrar las columnas para que coincidan con la tabla 'canciones'
        df_merged = df_merged.rename(columns = {
            'Nombre': 'nombre',
            'Duración (segundos)': 'duracion_segundos',
            'Popularidad': 'popularidad',
            'Explícito': 'explicito',
            'Fecha de Lanzamiento': 'fecha_lanzamiento',
            'Danceability': 'danceability',
            'Energy': 'energy',
            'Valence': 'valence',
            'Tempo': 'tempo',
            'Acousticness': 'acousticness',
            'Instrumentalness': 'instrumentalness',
            'Speechiness': 'speechiness',
            
        })

        # Convertir 'artista_id' a int64 si no hay valores nulos
        if df_merged['artista_id'].notnull().all():
            df_merged['artista_id'] = df_merged['artista_id'].astype(int)
        else:
            print("Existen valores nulos en 'artista_id'. No se puede convertir.")

        # Agregar columna 'nombre' al DataFrame antes de la inserción
        df_merged['nombre'] = df_merged['nombre'].fillna('Desconocido') 

        # Verificar las columnas finales en df_merged
        print('Columnas en df_merged:', df_merged.columns)
        print('')
        print(' ----- ----- Soy un separador ----- ----- ')
        print('')

        # Verificar que las columnas a insertar esten presentes
        columnas_a_insertar = ['artista_id', 'duracion_segundos', 'popularidad', 'explicito', 
                                'fecha_lanzamiento', 'danceability', 'energy', 'valence', 
                                'tempo', 'acousticness', 'instrumentalness', 'speechiness', 'nombre']

        # Imprimir columnas faltantes
        faltan_columnas = [col for col in columnas_a_insertar if col not in df_merged.columns]
        if faltan_columnas:
            print(f'Las siguientes columnas no están en df_merged: {faltan_columnas}')
        else:
            df_merged[columnas_a_insertar].to_sql('canciones', con = engine, if_exists = 'append', index = False)

    except SQLAlchemyError as e:
        print(f"Error al cargar datos en la base de datos: {e}")
    finally:
        if connection:
            connection.close()

        