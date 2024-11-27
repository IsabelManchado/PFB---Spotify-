# -*- coding: utf-8 -*-
"""graficos_sprint_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PsPorU-DSEfl1_EE-BM5QkFMJI_55mzV
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots

# from google.colab import files
# uploaded = files.upload()

df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
# df

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def graficos_sprint_2(df):
    genre_counts = df['predicted_genre'].value_counts().reset_index()
    genre_counts.columns = ['Género', 'Conteo']

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='Conteo',
        y='Género',
        data=genre_counts.head(10),
        palette='viridis'
    )
    plt.title('Géneros Más Escuchados en la Lista de Reproducción')
    plt.xlabel('Conteo')
    plt.ylabel('Género')
    plt.show()

    scatter_valence_speechiness = px.scatter(
        df,
        x='valence',
        y='speechiness',
        color='popularidad',
        size='popularidad',
        hover_name='nombre',
        title='Relación entre Valence (Felicidad) y Speechiness',
        labels={"Valence": "Valence (Felicidad)", "Speechiness": "Speechiness"}
    )
    scatter_valence_speechiness.show()

    explicit_counts = df['explícito'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(
        explicit_counts,
        labels=explicit_counts.index,
        autopct='%1.1f%%',
        colors=['#66c2a5', '#fc8d62'],
        startangle=140
    )
    plt.title('Distribución de Canciones "Explícitas"')
    plt.show()

    

    mean_values = df[['danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'instrumentalness', 'speechiness',
                      'popularidad', 'duración (segundos)']].mean()

    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=mean_values.values,
        theta=mean_values.index,
        fill='toself',
        name='Media de Atributos'
    ))
    radar_fig.update_layout(
        title='Media de Atributos de la Lista de Reproducción',
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        )
    )
    radar_fig.show()

    df['artistas'] = df['artistas'].astype(str)
    all_artists = df['artistas'].str.split(', ')
    flattened_artists = all_artists.explode()
    artist_counts = flattened_artists.value_counts().reset_index()
    artist_counts.columns = ['Artista', 'Count']
    top_artists = artist_counts.head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='Count',
        y='Artista',
        data=top_artists,
        palette='viridis'
    )
    plt.title('Artistas Más Escuchados en la Lista de Reproducción (Conteo Total)')
    plt.xlabel('Número de Canciones')
    plt.ylabel('Artista')
    plt.show()

    top_10_artists = artist_counts.head(10)['Artista']
    df_exploded = df.explode('artistas')
    mean_popularity = df_exploded[df_exploded['artistas'].isin(top_10_artists)].groupby('artistas')['popularidad'].mean().reset_index()
    mean_popularity = mean_popularity.sort_values(by='popularidad', ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='popularidad',
        y='artistas',
        data=mean_popularity,
        palette='viridis'
    )
    plt.title('Popularidad Media de los 10 Mejores Artistas en la Lista de Reproducción')
    plt.xlabel('Popularidad Media')
    plt.ylabel('Artista')
    plt.show()

    quantitative_columns = ['danceability', 'energy', 'valence', 'tempo',
                            'acousticness', 'instrumentalness', 'speechiness',
                            'popularidad', 'duración (segundos)']
    corr_matrix = df[quantitative_columns].corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index
    ))
    heatmap.show()

# graficos_sprint_2(df)

#Modificacion del código de Paola por Isa para poder llamar por separado a cada gráfico:

def grafico_genero(df):
    genre_counts = df['predicted_genre'].value_counts().reset_index()
    genre_counts.columns = ['Género', 'Conteo']
    plt.style.use("dark_background")
    fig=plt.figure(figsize=(12, 18))
    ax=sns.barplot(
        x='Conteo',
        y='Género',
        data=genre_counts.head(10),
        palette='viridis'
    )
    ax.set_title('Géneros Más Escuchados en la Lista de Reproducción')
    ax.set_xlabel('Conteo')
    ax.set_ylabel('Género')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig) 

def grafico_artistas1(df):
    df['artistas'] = df['artistas'].astype(str)
    all_artists = df['artistas'].str.split(', ')
    flattened_artists = all_artists.explode()
    artist_counts = flattened_artists.value_counts().reset_index()
    artist_counts.columns = ['Artista', 'Count']
    top_artists = artist_counts.head(10)

    fig=plt.figure(figsize=(12, 22))
    ax=sns.barplot(
        x='Count',
        y='Artista',
        data=top_artists,
        palette='viridis'
    )
    ax.set_title('Artistas Más Escuchados en la Lista de Reproducción (Conteo Total)')
    ax.set_xlabel('Número de Canciones')
    ax.set_ylabel('Artista')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig)  

def atributos(df):
    # Calcular las medias para los dos conjuntos de atributos
    mean_values1 = df[['danceability', 'energy', 'valence',
                       'acousticness', 'instrumentalness', 'speechiness']].mean()
    mean_values2 = df[['tempo', 'popularidad', 'duración (segundos)']].mean()

    # Crear subplots con dos gráficos de radar
    fig = make_subplots(
        rows=1, cols=2,  # Una fila y dos columnas
        specs=[[{'type': 'polar'}, {'type': 'polar'}]],  # Tipo de subplot polar para gráficos de radar
        subplot_titles=("Media de Atributos del Grupo 1", "Media de Atributos del Grupo 2")
    )

    # Gráfico de radar para mean_values1
    fig.add_trace(go.Scatterpolar(
        r=mean_values1.values,
        theta=mean_values1.index,
        fill='toself',
        name='Media de Atributos 1'
    ), row=1, col=1)

    # Gráfico de radar para mean_values2
    fig.add_trace(go.Scatterpolar(
        r=mean_values2.values,
        theta=mean_values2.index,
        fill='toself',
        name='Media de Atributos 2'
    ), row=1, col=2)

    # Configurar el layout del gráfico en modo oscuro
    fig.update_layout(
    template='plotly_dark',
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    )
)

    
    return st.plotly_chart(fig)

def graficos_extras(df):

    fig = make_subplots(
        rows=3, cols=1,  # Una fila y dos columnas
        specs=[
        [{'type': 'xy'}],       # Primera fila con gráfico de dispersión (scatter)
        [{'type': 'domain'}],   # Segunda fila con gráfico de pastel (pie)
        [{'type': 'heatmap'}]   # Tercera fila con gráfico de calor (heatmap)
    ],   
        subplot_titles=("Relación entre dos Variables", "Distribución de Canciones 'Explícitas'","Mapa de calor"),
        vertical_spacing=0.1
    )
    fig.add_trace(go.Scatter(
            x=df['valence'],
            y=df['speechiness'],
            mode='markers',
            marker=dict(
                size=df['popularidad'] / 10,  # Ajuste del tamaño
                color=df['popularidad'],
                showscale=True,
                colorbar=dict(title="Popularidad",x=1.15,
                    y=0.9,len=0.4)
            ),
            name="Valence vs. Speechiness"
            
        ),row=1, col=1)
    

    explicit_counts = df['explícito'].value_counts()
    
    fig.add_trace(go.Pie(
        
        labels=explicit_counts.index,
        values=explicit_counts.values,
        hole=0.3,
        textinfo='percent+label'
    ),row=2, col=1)
    

    quantitative_columns = ['danceability', 'energy', 'valence', 'tempo',
                            'acousticness', 'instrumentalness', 'speechiness',
                            'popularidad', 'duración (segundos)']
    corr_matrix = df[quantitative_columns].corr()

    fig.add_trace(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        coloraxis="coloraxis",
    ),row=3, col=1)

    fig.update_layout(
        template='plotly_dark',
        height=1200, 
        coloraxis=dict(
            colorscale='Viridis',
            colorbar=dict(
                title="Correlación",
                x=1.15,  
                y=0.1,
                len=0.4  
            )
        ),
        legend=dict(
            x=1.15,       # Posición horizontal de la leyenda
            y=0.55,       # Posición vertical para que esté centrada con el gráfico de pastel
            traceorder="normal",
            font=dict(size=10),
        ),
        title_text="Gráficos Extras de la Lista de Reproducción"
    )

    return st.plotly_chart(fig)

def comparador_genero(playlist_id1,playlist_id2):
    df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on="Canción ID", right_on="canción id")

    df_playlist_stats = df_playlist_canciones.groupby(['Playlist ID', 'predicted_genre']).size().reset_index()
    df_playlist_stats.columns = ['Playlist ID','Género', 'Conteo']
    playlists_filtradas = [playlist_id1, playlist_id2]  
    df_filtrado = df_playlist_stats[df_playlist_stats['Playlist ID'].isin(playlists_filtradas)]
    plt.style.use("dark_background")
    fig=plt.figure(figsize=(12, 18))
    ax=sns.barplot(
        x='Conteo',
        y='Género',
        hue="Playlist ID",
        data=df_filtrado,
        palette='viridis',
        
    )
    ax.set_title('Géneros Más Escuchados en la Lista de Reproducción')
    ax.set_xlabel('Conteo')
    ax.set_ylabel('Género')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig) 

def comparador_artistas(playlist_id1,playlist_id2):

    df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on="Canción ID", right_on="canción id")
    artist_counts = df_playlist_canciones.groupby(['Playlist ID', 'artistas']).size().reset_index()


    # df_canciones['artistas'] = df_canciones['artistas'].astype(str)
    # all_artists = df_canciones['artistas'].str.split(', ')
    # flattened_artists = all_artists.explode()
    # artist_counts = flattened_artists.value_counts().reset_index()
    artist_counts.columns = ['Playlist ID','Artista', 'Count']
    playlists_filtradas = [playlist_id1, playlist_id2]  
    df_filtrado = artist_counts[artist_counts['Playlist ID'].isin(playlists_filtradas)]
    top_artist=df_filtrado.sort_values(by=["Count"], ascending=False).head(15)

    fig=plt.figure(figsize=(12, 22))
    ax=sns.barplot(
        x='Count',
        y='Artista',
        hue='Playlist ID',
        data=top_artist,
        palette='viridis'
    )
    ax.set_title('Artistas Más Escuchados en la Lista de Reproducción (Conteo Total)')
    ax.set_xlabel('Número de Canciones')
    ax.set_ylabel('Artista')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig)  

def comparador_atributos(playlist_id1,playlist_id2):
    df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on="Canción ID", right_on="canción id")
    mean_features=['Playlist ID','danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'instrumentalness', 'speechiness',
                      'popularidad', 'duración (segundos)']
    df_mean = df_playlist_canciones[mean_features]
    
    # Calcular medias por Playlist ID
    df = df_mean.groupby('Playlist ID').mean().reset_index()

    # Filtrar las playlists específicas
    playlists_filtradas = [playlist_id1, playlist_id2]
    df_filtrado = df[df['Playlist ID'].isin(playlists_filtradas)]
    
    # Definir atributos para cada radar
    features_1 = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']
    features_2 = ['tempo', 'popularidad', 'duración (segundos)']
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=("Media de Atributos del Grupo 1", "Media de Atributos del Grupo 2"))
    
    for playlist_id in playlists_filtradas:
            # Filtrar datos para la playlist actual
            df_1 = df_filtrado[df_filtrado['Playlist ID'] == playlist_id][features_1].mean()
            df_2 = df_filtrado[df_filtrado['Playlist ID'] == playlist_id][features_2].mean()
            
            # Gráfico de radar para features_1
            fig.add_trace(go.Scatterpolar(
                r=df_1.values,
                theta=features_1,
                fill='toself',
                name=f'Playlist {playlist_id} - Atributos 1'
            ), row=1, col=1)

            # Gráfico de radar para features_2
            fig.add_trace(go.Scatterpolar(
                r=df_2.values,
                theta=features_2,
                fill='toself',
                name=f'Playlist {playlist_id} - Atributos 2'
            ), row=1, col=2)

        # Configurar el layout del gráfico
    fig.update_layout(
        template='plotly_dark',
        polar=dict(radialaxis=dict(visible=True)),
        title="Comparación de Atributos entre Playlists"
    )

    # Mostrar el gráfico en Streamlit
    
    
    return st.plotly_chart(fig)





# def grafico_artistas2(df):
#     df['artistas'] = df['artistas'].astype(str)
#     all_artists = df['artistas'].str.split(', ')
#     flattened_artists = all_artists.explode()
#     artist_counts = flattened_artists.value_counts().reset_index()
#     top_10_artists = artist_counts.head(10)['artistas']
#     df_exploded = df.explode('artistas')
#     mean_popularity = df_exploded[df_exploded['artistas'].isin(top_10_artists)].groupby('artistas')['popularidad'].mean().reset_index()
#     mean_popularity = mean_popularity.sort_values(by='popularidad', ascending=False)

#     fig=plt.figure(figsize=(12, 6))
#     ax=sns.barplot(
#         x='popularidad',
#         y='artistas',
#         data=mean_popularity,
#         palette='viridis'
#     )
#     ax.set_title('Popularidad Media de los 10 Mejores Artistas en la Lista de Reproducción')
#     ax.set_xlabel('Popularidad Media')
#     ax.set_ylabel('Artista')
#     return st.pyplot(fig) 