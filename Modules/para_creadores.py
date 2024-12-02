import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from Modules.graficos_playlist import graficos, pc_pregunta1, pc_pregunta2, pc_pregunta3, pc_pregunta4, pc_pregunta5, pc_pregunta6, pc_pregunta7
from menu import menu_stream
# Configuración de la página
st.set_page_config(
    page_title="Spotify Recommender App",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Activar tema oscuro en Altair
alt.themes.enable("dark")
menu, option = menu_stream(context= "para_creadores")


# Título principal
st.title("Para creadores")

# Cargar el DataFrame
try:
    df = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")
except FileNotFoundError:
    st.error("El archivo no se encuentra. Verifica la ruta.")
    df = None

# Solo ejecutar el resto del código si el DataFrame fue cargado correctamente
if df is not None:

 def para_creadores(df):
    # PREGUNTA 1
    with st.container():
        col1, col2 = st.columns([2, 4])

        # Columna 1: Texto
        with col1:
            st.subheader("¿Qué valores se relacionan?")
            st.write(
                "Aquí puedes ver cuáles características de las tracks son más relevantes y relacionadas para llegar a la popularidad."
            )

        # Columna 2: Gráfico de calor
        with col2:
            try:
                pc_pregunta1(df)
            except Exception as e:
                st.error(f"Error al generar el gráfico de calor: {e}")

    # PREGUNTA 2
    with st.container():
        col1, col2 = st.columns([4, 2])

        # Columna 1: Gráfico de dispersión
        with col1:
            try:
                pc_pregunta2(df)
            except Exception as e:
                st.error(f"Error al generar el gráfico de dispersión: {e}")

        # Columna 2: Texto descriptivo
        with col2:
            st.subheader("¿La popularidad se relaciona con la “felicidad”?")
            st.write(
                "Aquí puedes analizar si existe alguna relación entre la popularidad y el valence (una medida de felicidad o positividad)."
            )

    # PREGUNTA 3
    with st.container():
        col1, col2 = st.columns([2, 4])

        # Columna 1: Texto
        with col1:
            st.subheader("¿Y el ritmo es importante?")
            st.write(
                "Aquí puedes ver cuáles características de las tracks son más relevantes y relacionadas para llegar a la popularidad."
            )

        # Columna 2: Histograma
        with col2:
            try:
                pc_pregunta3(df)
            except Exception as e:
                st.error(f"Error al generar el histograma: {e}")

    # PREGUNTA 4
    with st.container():
        col1, col2 = st.columns([4, 2])

        # Columna 1: Texto
        with col1:
            try:
                pc_pregunta4(df)
            except Exception as e:
             st.error(f"Error al generar el gráfico: {e}")
            

        # Columna 2: Gráfico combinado
        with col2:
            st.subheader("¿En qué años salieron las tracks más populares?")
            st.write(
                "Aquí puedes analizar la distribución de las canciones populares a lo largo de los años."
            )
           


    with st.container():
        col1, col2 = st.columns([2, 4])

        # Columna 1: Texto
        with col1:
            st.title("Danceability")

        # Columna 2: Histograma
        with col2:
            st.write(
                """
            **Danceability** es una métrica utilizada en la música digital (como en Spotify) que indica qué tan adecuada 
            es una canción para bailar según sus características musicales. Este índice se calcula analizando varios elementos 
            de la canción, como el tempo, la estabilidad del ritmo, la fuerza del beat y los patrones generales.

            La puntuación de **danceability** se presenta en un rango de 0 a 1, donde los valores más altos indican canciones 
            más propensas a ser consideradas "bailables" y adecuadas para pistas de baile o entornos similares.
            """
            )

     # danceability 1 
    with st.container():
        col1, col2 = st.columns([2, 4])

        # Columna 1: Texto
        with col1:
            st.subheader("Danceability vs Energy")
            st.write(
                """
                El gráfico muestra que la mayoría de las canciones se concentran en valores medios tanto de "danceability" como de "energy", 
                alrededor de 0.6, lo que indica que las canciones más comunes tienen un equilibrio entre ritmo bailable y energía. 
                Sin embargo, también se observa una diversidad en las combinaciones, con algunas canciones ubicándose en los extremos 
                de estas métricas. Esto sugiere que, aunque las canciones balanceadas son más populares, existe una amplia variedad de estilos 
                musicales que abarca desde piezas muy enérgicas hasta aquellas menos bailables."
            
             """)
        # Columna 2: Histograma
        with col2:
            try:
                pc_pregunta5(df)
            except Exception as e:
                st.error(f"Error al generar el histograma: {e}")

     # PREGUNTA 6
    with st.container():
        col1, col2 = st.columns([4, 2])

        # Columna 1: Texto
        with col1:
            try:
                pc_pregunta6(df)
            except Exception as e:
             st.error(f"Error al generar el gráfico: {e}")
            

        # Columna 2: Gráfico combinado
        with col2:
            st.subheader("¿Cuántas tracks son “bailables”?")
            st.write(
                "Aquí puedes analizar la distribución de las canciones bailables "
            )

     # danceability 3
    with st.container():
        col1, col2 = st.columns([2, 4])

        # Columna 1: Texto
        with col1:
            st.subheader("¿Si es explícito se baila más?")
            st.write(
                """
                El gráfico muestra la distribución de Danceability en canciones explícitas y no explícitas. 
                Podemos observar que ambas categorías tienen una mediana similar en torno a 0.6, indicando que la mayoría 
                de las canciones, independientemente de si son explícitas o no, son moderadamente bailables. 
                Sin embargo, las canciones explícitas presentan una mayor variabilidad en sus valores, 
                lo que sugiere una diversidad más amplia en sus características rítmicas."
            
             """)
        # Columna 2: grafico 
        with col2:
            try:
                pc_pregunta7(df)
            except Exception as e:
                st.error(f"Error al generar el histograma: {e}")


# Llamada a la función principal
if __name__ == "__main__":
    para_creadores(df)

elif menu == "HomePage":
        exec(open("pruebahome.py").read())

elif menu == "Top Tracks":
        exec(open("top_tracks.py").read())
# Pie de página
st.markdown("---")
st.markdown(
    "Grupo B - HACK A BOSS - Hecho con ❤️ usando [Streamlit](https://streamlit.io)",
    unsafe_allow_html=True,
)
