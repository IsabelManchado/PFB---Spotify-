import streamlit as st
import pandas as pd
import pymysql


def app_bbdd():


        # Configuración de la conexión a la base de datos
    DB_CONFIG = {
        "user": "root",
        "password": "Jp261191.",
        "database": "Proyecto_Spotify",
        "host": "localhost",
        "port": 3306
    }

    def fetch_data(query):
        """Función para ejecutar una consulta SQL y devolver un DataFrame."""
        try:
            connection = pymysql.connect(**DB_CONFIG)
            df = pd.read_sql(query, connection)
            connection.close()
            return df
        except Exception as e:
            st.error(f"Error al conectar con la base de datos: {e}")
            return pd.DataFrame()

   

    # Título de la página
    st.title("Base de Datos")
    st.write("Explora la arquitectura de la base de datos utilizada en este proyecto. Aquí podrás ver las tablas, sus columnas y sus funciones.")
    
    # Sección: Diagrama de entidad-relación
    st.write("A continuación se muestra el diagrama de entidad-relación. Este diagrama muestra la relación entre las tablas principales de la base de datos. Cada tabla tiene su propósito, como almacenar información de artistas, canciones y playlists, que son utilizados en el funcionamiento del proyecto.")
    st.image('BBDD/Diagrama de entidad-relacion.png', caption = 'Diagrama de Entidad-Relación', use_column_width = True)
    
    # Explicación de las tablas
    st.subheader("Tablas y sus Funciones")
    
    # Sección de la Tabla Artistas
    with st.expander("**1. Artistas**"):
        st.markdown(""" 
        **Función**: Almacena los artistas registrados en la plataforma, con su identificador y nombre único.
        
        - **artista_id**: Identificador único del artista (clave primaria).
        - **nombre**: Nombre del artista, debe ser único.
        - **updated**: Fecha y hora de la última actualización del registro del artista.
        """, unsafe_allow_html = True)

        # Mostrar la tabla de Artistas extraída de MySQL
        query = "SELECT * FROM artistas"
        data = fetch_data(query)
        if not data.empty:
            st.dataframe(data, use_container_width = True)
        else:
            st.write("No se encontraron datos en la tabla Artistas.")
    
    # Sección de la Tabla Canciones
    with st.expander("**2. Canciones**"):
        st.markdown(""" 
        **Función**: Almacena las canciones disponibles en la plataforma, asociadas a un artista, con información detallada sobre su duración, popularidad y atributos musicales.

        - **cancion_id**: Identificador único de la canción (clave primaria).
        - **nombre**: Nombre de la canción.
        - **artista_id**: Identificador del artista asociado (clave foránea de la tabla artistas).
        - **duracion_segundos**: Duración de la canción en segundos.
        - **popularidad**: Popularidad de la canción, en una escala de 0 a 100.
        - **explicito**: Indica si la canción tiene contenido explícito (booleano).
        - **fecha_lanzamiento**: Fecha en que se lanzó la canción.
        - **danceability**: Medida de la facilidad de la canción para bailar (rango de 0 a 1).
        - **energy**: Nivel de energía de la canción (rango de 0 a 1).
        - **valence**: Estado emocional de la canción (rango de 0 a 1).
        - **tempo**: Tempo de la canción (en BPM).
        - **acousticness**: Nivel de acústica de la canción (rango de 0 a 1).
        - **instrumentalness**: Proporción de música instrumental en la canción (rango de 0 a 1).
        - **speechiness**: Indica la cantidad de palabras habladas en la canción (rango de 0 a 1).
        - **url_spotify**: Enlace a la canción en Spotify.
        - **imagen**: URL o ruta de la imagen asociada a la canción.
        - **updated**: Fecha y hora de la última actualización de los datos de la canción.
        """, unsafe_allow_html = True)

        # Mostrar la tabla de Canciones extraída de MySQL
        query = "SELECT * FROM canciones"
        data = fetch_data(query)
        if not data.empty:
            st.dataframe(data, use_container_width = True)
        else:
            st.write("No se encontraron datos en la tabla Canciones.")
    
    # Sección de la Tabla Playlist
    with st.expander("**3. Playlist**"):
        st.markdown(""" 
        **Función**: Relaciona las canciones con las playlists en las que están contenidas. Cada fila indica que una canción pertenece a una playlist específica.

        - **cancion_id**: Identificador único de la canción asociada a la playlist (clave foránea de la tabla canciones).
        - **playlist_id**: Identificador único de la playlist.
        - **updated**: Fecha y hora de la última actualización del registro de la playlist.
        """, unsafe_allow_html = True)

        # Mostrar la tabla de Playlist extraída de MySQL
        query = "SELECT * FROM playlist"
        data = fetch_data(query)
        if not data.empty:
            st.dataframe(data, use_container_width = True)
        else:
            st.write("No se encontraron datos en la tabla Playlist.")

if __name__ == "__main__":
    app_bbdd()
