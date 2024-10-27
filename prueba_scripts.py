
import streamlit as st
from Modules.EDA import collect_data
from Modules.BBDD import creacion_database, load_data
import pymysql


def eda_app():
    st.title("Spotify Playlist")

    # Entrada para ID de la playlist y base de datos
    playlist_id = st.text_input("Ingresa el ID de la playlist de Spotify:")
    database = "Proyecto_Spotify"

    # Botón para ejecutar el proceso
    if st.button("Ejecutar"):
        if playlist_id:
            st.write("Iniciando recopilación de datos...")
            raw_data = collect_data(playlist_id)
            #st.write("Creando base de datos...")
            #creacion_database(database)
            st.write("Datos recopilados y base de datos creada. Cargando base de datos...")
            loaded_data = load_data(raw_data)
            st.write("Datos cargados")
            st.success("Proceso completado y datos cargados a la base de datos.")
            st.dataframe(collect_data(playlist_id))
        else:
            st.warning("Por favor, ingresa un ID de playlist válido.")

if __name__ == "__main__":
    eda_app()
