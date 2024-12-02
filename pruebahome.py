import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from menu import menu_stream
import subprocess
import top_tracks

# Configuración de la página
st.set_page_config(
    page_title="Spotify Recommender App",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#  tema oscuro en Altair
alt.themes.enable("dark")

    # Llamar al menú
menu, option = menu_stream(context = "pruebahome")
# Función principal
def homepage():


    if menu == "HomePage":
        # Primer contenedor: Logo y título
        with st.container():
            col1, col2 = st.columns([1, 6])

            # Columna 1: Logo
            with col1:
                st.image("Modules/logo.PNG", width=900, use_column_width="always")

            # Columna 2: Título principal
            with col2:
                st.markdown(
                    "<h1 style='text-align: left;'>Recomendador Spotify App</h1>",
                    unsafe_allow_html=True,
                )

        # Segunda sección: Contenido principal con dos columnas
        with st.container():
            col1, col2 = st.columns([2, 6])

            # Columna 1: Botón
            with col1:
                st.subheader("Encuentra las mejores playlist y canciones")
                st.write(
                    "Recomendador Spotify App es tu nueva herramienta gratuita para descubrir música sin límites."
                )
                if st.button("Busca tu playlist"):
                    st.success("¡Explorando playlists!")

            # Columna 2: Imagen grande
            with col2:
                st.image("Modules/home.jpg", use_column_width=False, width=700)

    elif menu == "Top Tracks":
        top_tracks.app()

    elif menu == "Para creadores":
        exec(open("para_creadores.py", encoding="utf-8").read())


    elif menu == "Comparador":
        exec(open("app_comparador.py", encoding="utf-8").read())
        subprocess.run(["python", "app_comparador.py"])

    elif menu == "Recomendador":
        exec(open("app_recomendador.py", encoding="utf-8").read())

    elif menu == "Base de datos":
        exec(open("app_bbdd.py", encoding="utf-8").read())

    elif menu == "Cómo y porqué":
        exec(open("app_whyandhow.py", encoding="utf-8").read())

    elif menu == "About":
        exec(open("app_aboutus.py", encoding="utf-8").read())

    # Pie de página
    st.markdown("---")
    st.markdown(
        "Grupo B - HACK A BOSS - Hecho con ❤️ usando [Streamlit](https://streamlit.io)",
        unsafe_allow_html=True,
    )


# Ejecutar la función principal
if __name__ == "__main__":
    homepage()
