import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from menu import menu_stream
from top_tracks import top_tracks
from app_comparador import app_comparador
from app_recomendador import app_recomendador
from app_aboutus import about
from app_whyandhow import whyandhow
from para_creadores import para_creadores
from app_bbdd import app_bbdd






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
        top_tracks()

    elif menu == "Para creadores":
        df = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")
        para_creadores(df)


    elif menu == "Comparador":
        app_comparador()

    elif menu == "Recomendador":
        app_recomendador()

    elif menu == "Base de datos":
        app_bbdd()

    elif menu == "Cómo y porqué":
        whyandhow()

    elif menu == "About":
        about()

    # Pie de página
    st.markdown("---")
    st.markdown(
        "Grupo B - HACK A BOSS - Hecho con ❤️ usando [Streamlit](https://streamlit.io)",
        unsafe_allow_html=True,
    )


# Ejecutar la función principal
if __name__ == "__main__":
    homepage()
