import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
from Modules.graficos_sprint_2 import grafico_genero, grafico_artistas1, explicit_top_tracks
from menu import menu_stream

st.title("Top Tracks")

    # Llamar al menú
menu, option = menu_stream(context= "top_tracks")

def top_tracks():
    # Contenedor principal para los gráficos
    with st.container():
        col1, col2 = st.columns([1, 1])

        # Cargar el archivo CSV
        try:
            df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
        except FileNotFoundError:
            st.error("El archivo no se encuentra. Verifica la ruta.")
            return
        except Exception as e:
            st.error(f"Error al cargar el archivo CSV: {e}")
            return

        # Columna 1: Gráfico de Artistas
        with col1:
            st.subheader("Top artistas")
            try:
                grafico_artistas1(df)
            except Exception as e:
                st.error(f"Error al generar el gráfico de artistas: {e}")

        # Columna 2: Gráfico de Géneros
        with col2:
            st.subheader("Top géneros")
            try:
                grafico_genero(df)
            except Exception as e:
                st.error(f"Error al generar el gráfico de géneros: {e}")

    # Contenedor para los textos descriptivos (debajo de los gráficos)
    with st.container():
        col1, col2 = st.columns([1, 1])

        # Columna 1: Texto sobre los artistas
        with col1:
            st.subheader("¿Quiénes son los artistas más populares del momento?")
            st.write(
                "Aquí te mostramos un ranking de los 10 artistas más escuchados del momento."
            )

        # Columna 2: Texto sobre los géneros
        with col2:
            st.subheader("¿Cuáles géneros son los más escuchados?")
            st.write(
                "Este gráfico muestra cuáles son los géneros musicales con más reproducciones actualmente."
            )

        st.markdown(
            "<h2 style='text-align: center; color: green;'>¿Cuántas canciones explícitas son muy famosas ahora?</h2>",
            unsafe_allow_html=True,
        )   
    with st.container():
    
        try:
            df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
            explicit_top_tracks(df)
        except Exception as e:
            # Mostrar mensaje de error si ocurre una excepción
            st.error(f"Error al generar el gráfico: {e}")

    # Pie de página
    st.markdown("---")
    st.markdown(
        "Grupo B - HACK A BOSS - Hecho con ❤️ usando [Streamlit](https://streamlit.io)",
        unsafe_allow_html=True,
    )


# Llamada a la función principal
if __name__ == "__main__":
    top_tracks()

elif menu == "HomePage":
        exec(open("pruebahome.py").read())

elif menu == "Para creadores":
        exec(open("para_creadores.py").read())