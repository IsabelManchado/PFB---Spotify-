

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#from google.colab import files
#uploaded = files.upload()

"""#Análisis preliminar de datos:
En esa parte vamos a crear algunos gráficos básicos para entender mejor las relaciones entre variables de los datos extraídos.
"""

"""## Relaciones entre variables del DF

##Correlación Heatmap entre variables
Las celdas con color más claro indican las relaciones positivas, por ejemplo podemos notar que Danceability y Energy nos comunica que las canciones más intensas son las que se puede bailar con más facilidad.
"""
def graficos(df):
    
    quantitative_columns = ['Danceability', 'Energy', 'Valence', 'Tempo', 'Acousticness', 'Instrumentalness', 'Speechiness', 'Popularidad', 'Duración (segundos)']
    corr_matrix = df[quantitative_columns].corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,

    ))
    heatmap.update_layout(title="Correlación Heatmap entre variables")
    #heatmap.show()

    """ ## Bubble Chart: Valence vs Popularity

    Este código genera un Bubble Chart para analizar la relación entre la variable "Valence", indicador de cuando es alegra la cancion, y "Polularidad" de la Playlist.
    Las bolas indican cada canción y su dimensión corresponde a "Duración" en segundos de la misma.

    """

    bubble = px.scatter(
        df,
        x='Valence',
        y='Popularidad',
        size='Duración (segundos)',
        color='Duración (segundos)',
        hover_name='Nombre',
        title='Valence vs Popularity',
        labels={"Valence": "Valence (Happiness)", "Popularidad": "Popularity"})
    #bubble.show()

    """## Scatter Plot: Danceability vs Energy
    Este Scatter Plot permite analizar cómo se relacionan la bailabilidad y la energía de las canciones en la playlist, destacando además la popularidad de cada canción mediante el color y el tamaño de los puntos. Es útil para identificar patrones entre estos atributos y entender la diversidad de la playlist
    """

    scatter = px.scatter(
        df,
        x='Danceability',
        y='Energy',
        color='Popularidad',
        size='Popularidad',
        hover_name='Nombre',
        title='Danceability vs Energy',
        labels={"Danceability": "Danceability", "Energy": "Energy"}
    )
    #scatter.show()

    """## Histograma distribución de Tempo
    La variable Tempo representa los BPM, o sea  Beats Per Minute (pulsos por minuto) y es una unidad que mide la velocidad o ritmo de una canción.
    Este Histograma indica la distribución de los valores de Tempo en la playlist, identificando qué rangos de BPM son más comunes entre las canciones
    """

    # Histogram della distribuzione di Tempo - Playlist
    hist = px.histogram(
        df,
        x='Tempo',
        nbins=10,
        title='Distribución de Tempo (BPM)',
        labels={"Tempo": "Tempo (BPM)"}
    )
    #hist.show()

    """## Box Plot: Distribución de Danceability

    Este código crea un Box Plot que muestra la distribución de Danceability (bailabilidad) de las canciones en la playlist.
    visualizar la dispersión y variabilidad de la bailabilidad entre las canciones.


    """

    box_plot = px.box(
        df,
        y='Danceability',
        points="all",
        title='Distribución de Danceability'
    )
    #box_plot.show()

    """## Distribución de Danceability en canciones "Explicit"
    Con este gráfico podemos analizar la distribución de la Danceability, dividiendo los resultados para canciones con etiqueta explicit y las que no.
    """

    violin = px.violin(
        df,
        y='Danceability',
        x='Explícito',
        box=True,
        points="all",
        title='Distribución de Danceability en canciones "Explicit"'
    )
    #violin.show()

    """## Area Plot : Tendencia de Popularidad en el tiempo
    Con este gráfico podemos ver como ha cambiado la popularidad con base en la fecha de estreno de una canción
    """

    df['Fecha de Lanzamiento'] = pd.to_datetime(df['Fecha de Lanzamiento'])
    area = px.area(
        df.sort_values('Fecha de Lanzamiento'),
        x='Fecha de Lanzamiento',
        y='Popularidad',
        title='Tendencia de Popularidad en el tiempo'
    )
    #area.show()

    # """## Radar Chart: Visualizacion del perfil de la cancion"""

    # song_name = input("Nombre cancion deseada: ")


    # selected_song = df[df['Nombre'] == song_name]


    # if selected_song.empty:
    #     print("La canzone inserita non è presente nel dataset.")
    # else:

    #     song_data = selected_song.iloc[0]


    #     radar_fig = go.Figure()

    #     radar_fig.add_trace(go.Scatterpolar(
    #         r=[
    #             song_data['Danceability'], song_data['Energy'], song_data['Valence'],
    #             song_data['Acousticness'], song_data['Instrumentalness'], song_data['Speechiness']
    #         ],
    #         theta=['Danceability', 'Energy', 'Valence', 'Acousticness', 'Instrumentalness', 'Speechiness'],
    #         fill='toself',
    #         name=song_data['Nombre']
    #     ))

    #     radar_fig.update_layout(title=f"Perfil: {song_name}")
    #     #radar_fig.show()
   
    return heatmap, bubble, scatter, hist, box_plot, violin, area #, radar_fig

import plotly.graph_objects as go

def pc_pregunta1(df):
    quantitative_columns = [
        'danceability', 'energy', 'valence', 'tempo', 
        'acousticness', 'instrumentalness', 'speechiness', 
        'popularidad', 'duración (segundos)'
    ]

    # Calcular la matriz de correlación
    corr_matrix = df[quantitative_columns].corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale="Viridis"
    ))
    st.plotly_chart(heatmap, use_container_width=True)


def pc_pregunta2(df):

    """
    Genera un gráfico de líneas de contorno para analizar la densidad de Valence vs Popularidad.
    """
    try:
        df_prueba = df.sample(frac=0.05, random_state=42)  # Tomar solo el 5% de los datos

        fig = px.density_contour(
            df_prueba,
            x="valence",
            y="popularidad",
            title="Densidad de Valence vs Popularity (Contornos)",
            labels={"valence": "Valence (Happiness)", "popularidad": "Popularity"},
        )

        fig.update_layout(
            paper_bgcolor="black",  
            plot_bgcolor="black",  
            font=dict(color="white"),  
        )

        st.plotly_chart(fig, use_container_width=True)

    except KeyError as e:
        st.error(f"Error: Falta la columna {e} en el DataFrame.")
    except Exception as e:
        st.error(f"Error al generar el gráfico de contornos: {e}")



def pc_pregunta3(df):
        plt.figure(figsize=(8, 6))
        plt.style.use('dark_background')
        plt.hist(df['tempo'], bins=30, alpha=0.7)  
        plt.title('Distribución del Ritmo (Tempo)')
        plt.xlabel('Tempo (BPM)')
        plt.ylabel('Frecuencia')
        st.pyplot(plt, use_container_width=True)  

def pc_pregunta4(df):

    try:
        df['fecha de lanzamiento'] = pd.to_datetime(df['fecha de lanzamiento'], errors='coerce')
        df = df.dropna(subset=['fecha de lanzamiento'])

        
        area = px.area(
            df.sort_values('fecha de lanzamiento'),   
            x='fecha de lanzamiento',
            y='popularidad',
            title='Tendencia de Popularidad en el Tiempo',
            labels={'fecha de lanzamiento': 'Fecha de Lanzamiento', 'popularidad': 'Popularidad'},
        )

        
        area.update_layout(
            paper_bgcolor="black",  
            plot_bgcolor="black",  
            font=dict(color="white")  
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(area, use_container_width=True)

    except KeyError as e:
        st.error(f"Error: Falta la columna {e} en el DataFrame.")
    except Exception as e:
        st.error(f"Error al generar el gráfico: {e}")

def pc_pregunta5(df):

    """
    Genera un gráfico de líneas de contorno para analizar la densidad de Valence vs Popularidad.
    """

    df_prueba = df.sample(frac=0.05, random_state=42)  # Tomar solo el 5% de los datos

    fig = px.density_contour(
            df_prueba,
            x="danceability",
            y="energy",
            title="Densidad de Danceability vs Energy (Contornos)",
            labels={"danceability": "Danceability", "energy": "energy"},
        )

    fig.update_layout(
            paper_bgcolor="black",  
            plot_bgcolor="black",  
            font=dict(color="white"),  
        )

    st.plotly_chart(fig, use_container_width=True)

def pc_pregunta6(df):
    df_prueba = df.sample(frac=0.05, random_state=42)
    box_plot = px.box(
            df_prueba,
            y='danceability',
            points="all",  
            title='Distribución de Danceability',
            labels={'danceability': 'Danceability'},
        )

        
    box_plot.update_layout(
            paper_bgcolor="black",  
            plot_bgcolor="black",  
            font=dict(color="white")  
        )

       
    st.plotly_chart(box_plot, use_container_width=True)

def pc_pregunta7(df):
    violin = px.violin(
            df,
            y='danceability',
            x='explícito',
            box=True,  
            points="all",  
            title='Distribución de Danceability en canciones "Explícitas"',
            labels={'danceability': 'Danceability', 'explícito': 'Explícito'},
        )

        # Configuración de diseño
    violin.update_layout(
            paper_bgcolor="black",  
            plot_bgcolor="black",  
            font=dict(color="white")  
        )

        
    st.plotly_chart(violin, use_container_width=True)
