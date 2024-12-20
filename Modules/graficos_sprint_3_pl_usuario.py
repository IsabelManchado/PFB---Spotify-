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
from Modules.playlist_usuario import collect_data,predecir_genero_canciones


# from google.colab import files
# uploaded = files.upload()

# df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
# df

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def grafico_genero1(df):
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    # df_playlist_canciones = pd.merge(df_tracks, df, left_on="Canción ID", right_on="canción id")
    # playlist_filtrada = [playlist_id]
    # df_filtrado = df_playlist_canciones[df_playlist_canciones['Playlist ID'].isin(playlist_filtrada)]
    # genre_counts = df_filtrado['predicted_genre'].value_counts().reset_index()
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
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    # df_playlist_canciones = pd.merge(df_tracks, df, left_on="Canción ID", right_on="canción id")
    # df_playlist_canciones['artistas'] = df_playlist_canciones['artistas'].astype(str)
    # playlist_filtrada = [playlist_id]  
    # df_filtrado = df_playlist_canciones[df_playlist_canciones['Playlist ID'].isin(playlist_filtrada)]
    # all_artists = df_filtrado['artistas'].str.split(', ')
    all_artists = df['artistas'].str.split(', ')
    flattened_artists = all_artists.explode()
    artist_counts = flattened_artists.value_counts().reset_index()
    artist_counts.columns = ['Artista', 'Count']
    top_artists = artist_counts.head(10)
    plt.style.use("dark_background")
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

def atributos1(df) :
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    # df_playlist_canciones = pd.merge(df_tracks, df, left_on="Canción ID", right_on="canción id")
    # playlist_filtrada = [playlist_id]  
    # df_filtrado = df_playlist_canciones[df_playlist_canciones['Playlist ID'].isin(playlist_filtrada)]
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

def graficos_extras1(df):
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    # df_playlist_canciones = pd.merge(df_tracks, df, left_on="Canción ID", right_on="canción id")
    # playlist_filtrada = [playlist_id]  
    # df_filtrado = df_playlist_canciones[df_playlist_canciones['Playlist ID'].isin(playlist_filtrada)]

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
                size=df['popularidad']/3,  # Ajuste del tamaño
                color=df['popularidad'],
                showscale=True,
                colorbar=dict(title="Popularidad",x=1.15,
                    y=0.9,len=0.4)
            ),
            name="Valence vs. Speechiness"
            
        ),row=1, col=1)
    fig.update_layout(
        xaxis1=dict(
            title="Valence",
            range=[df['valence'].min(), df['valence'].max()]  
        ),
        yaxis1=dict(
            title="Speechiness",
            range=[df['speechiness'].min()-0.025, df['speechiness'].max()]  
        ),
        title="Valence vs Speechiness",
        height=600,
        width=800
    )
    

    explicit_counts = df['explícito'].value_counts()
    
    fig.add_trace(go.Pie(
        
        labels=explicit_counts.index,
        values=explicit_counts.values,
        hole=0.2,
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

def comparador_genero1(playlist_id1,playlist_id2):
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    # df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    # df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on="Canción ID", right_on="canción id")
    playlist_seleccionada1 = collect_data(playlist_id1)
    playlist_seleccionada2 = collect_data(playlist_id2)

    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    generos = ['pop', 'rock', 'hip hop', 'electronic', 'classical', 'jazz', 'country', 'latin']
    df_canciones1=predecir_genero_canciones(playlist_seleccionada1, client_id, client_secret, generos)
    df_canciones2=predecir_genero_canciones(playlist_seleccionada2, client_id, client_secret, generos)


    df_playlist_canciones = pd.concat([df_canciones1, df_canciones2], ignore_index=True)

    df_playlist_stats = df_playlist_canciones.groupby(['playlist', 'predicted_genre']).size().reset_index()
    df_playlist_stats.columns = ['Playlist','Género', 'Conteo']
    # playlists_filtradas = [playlist_id1, playlist_id2]  
    # df_filtrado = df_playlist_stats[df_playlist_stats['Playlist ID'].isin(playlists_filtradas)]
    plt.style.use("dark_background")
    fig=plt.figure(figsize=(12, 18))
    ax=sns.barplot(
        x='Conteo',
        y='Género',
        hue="Playlist",
        data=df_playlist_stats,
        palette='viridis',
        
    )
    ax.set_title('Géneros Más Escuchados en la Lista de Reproducción')
    ax.set_xlabel('Conteo')
    ax.set_ylabel('Género')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig) 

def comparador_artistas1(playlist_id1,playlist_id2):

    playlist_seleccionada1 = collect_data(playlist_id1)
    playlist_seleccionada2 = collect_data(playlist_id2)

    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    generos = ['pop', 'rock', 'hip hop', 'electronic', 'classical', 'jazz', 'country', 'latin']
    df_canciones1=predecir_genero_canciones(playlist_seleccionada1, client_id, client_secret, generos)
    df_canciones2=predecir_genero_canciones(playlist_seleccionada2, client_id, client_secret, generos)


    df_playlist_canciones = pd.concat([df_canciones1, df_canciones2], ignore_index=True)

    
    artist_counts = df_playlist_canciones.groupby(['playlist', 'artistas']).size().reset_index()


    # df_canciones['artistas'] = df_canciones['artistas'].astype(str)
    # all_artists = df_canciones['artistas'].str.split(', ')
    # flattened_artists = all_artists.explode()
    # artist_counts = flattened_artists.value_counts().reset_index()
    artist_counts.columns = ['Playlist','Artista', 'Count']
    # playlists_filtradas = [playlist_id1, playlist_id2]  
    # df_filtrado = artist_counts[artist_counts['Playlist ID'].isin(playlists_filtradas)]
    top_artist=artist_counts.sort_values(by=["Count"], ascending=False).head(15)

    fig=plt.figure(figsize=(12, 22))
    ax=sns.barplot(
        x='Count',
        y='Artista',
        hue='Playlist',
        data=top_artist,
        palette='viridis'
    )
    ax.set_title('Artistas Más Escuchados en la Lista de Reproducción (Conteo Total)')
    ax.set_xlabel('Número de Canciones')
    ax.set_ylabel('Artista')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig)  

def comparador_atributos1(playlist_id1,playlist_id2):
    playlist_seleccionada1 = collect_data(playlist_id1)
    playlist_seleccionada2 = collect_data(playlist_id2)

    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    generos = ['pop', 'rock', 'hip hop', 'electronic', 'classical', 'jazz', 'country', 'latin']
    df_canciones1=predecir_genero_canciones(playlist_seleccionada1, client_id, client_secret, generos)
    df_canciones2=predecir_genero_canciones(playlist_seleccionada2, client_id, client_secret, generos)


    df_playlist_canciones = pd.concat([df_canciones1, df_canciones2], ignore_index=True)


    mean_features=['playlist','danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'instrumentalness', 'speechiness',
                      'popularidad', 'duración (segundos)']
    df_mean = df_playlist_canciones[mean_features]
    
    # Calcular medias por Playlist ID
    df = df_mean.groupby('playlist').mean().reset_index()

    # Filtrar las playlists específicas
    # playlists_filtradas = [playlist_id1, playlist_id2]
    # df_filtrado = df[df['playlist'].isin(playlists_filtradas)]
    
    # Definir atributos para cada radar
    features_1 = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']
    features_2 = ['tempo', 'popularidad', 'duración (segundos)']
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=("Media de Atributos del Grupo 1", "Media de Atributos del Grupo 2"))
    
    valores_unicos = df['playlist'].unique().tolist()
    for playlist_id in valores_unicos:
            # Filtrar datos para la playlist actual
            df_1 = df[df['playlist'] == playlist_id][features_1].mean()
            df_2 = df[df['playlist'] == playlist_id][features_2].mean()
            
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


def comparador_genero_cancion(playlist_id1,playlist_id2,selected_song1,selected_song2):
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    # df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    # df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on="Canción ID", right_on="canción id")
    playlist_seleccionada1 = collect_data(playlist_id1)
    playlist_seleccionada2 = collect_data(playlist_id2)

    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    generos = ['pop', 'rock', 'hip hop', 'electronic', 'classical', 'jazz', 'country', 'latin']
    df_canciones1=predecir_genero_canciones(playlist_seleccionada1, client_id, client_secret, generos)
    df_canciones2=predecir_genero_canciones(playlist_seleccionada2, client_id, client_secret, generos)


    df_playlist_canciones = pd.concat([df_canciones1, df_canciones2], ignore_index=True)

    df_playlist_stats = df_playlist_canciones.groupby(['nombre', 'predicted_genre']).size().reset_index()
    filtered_df1 = df_playlist_stats[df_playlist_stats["Nombre"].isin([selected_song1, selected_song2])]
    filtered_df1.columns = ['Canción','Género', 'Conteo']
    # playlists_filtradas = [playlist_id1, playlist_id2]  
    # df_filtrado = df_playlist_stats[df_playlist_stats['Playlist ID'].isin(playlists_filtradas)]
    plt.style.use("dark_background")
    fig=plt.figure(figsize=(12, 18))
    ax=sns.barplot(
        x='Conteo',
        y='Género',
        hue="Canción",
        data=filtered_df1,
        palette='viridis',
        
    )
    ax.set_title('Géneros de las canciones')
    ax.set_xlabel('Conteo')
    ax.set_ylabel('Género')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig) 

def comparador_artistas_canciones(playlist_id1,playlist_id2,selected_song1,selected_song2):

    playlist_seleccionada1 = collect_data(playlist_id1)
    playlist_seleccionada2 = collect_data(playlist_id2)

    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    generos = ['pop', 'rock', 'hip hop', 'electronic', 'classical', 'jazz', 'country', 'latin']
    df_canciones1=predecir_genero_canciones(playlist_seleccionada1, client_id, client_secret, generos)
    df_canciones2=predecir_genero_canciones(playlist_seleccionada2, client_id, client_secret, generos)


    df_playlist_canciones = pd.concat([df_canciones1, df_canciones2], ignore_index=True)

    
    artist_counts = df_playlist_canciones.groupby(['nombre', 'artistas']).size().reset_index()
    filtered_df1 = artist_counts[artist_counts["Nombre"].isin([selected_song1, selected_song2])]


    # df_canciones['artistas'] = df_canciones['artistas'].astype(str)
    # all_artists = df_canciones['artistas'].str.split(', ')
    # flattened_artists = all_artists.explode()
    # artist_counts = flattened_artists.value_counts().reset_index()
    filtered_df1.columns = ['Canción','Artista', 'Count']
    # playlists_filtradas = [playlist_id1, playlist_id2]  
    # df_filtrado = artist_counts[artist_counts['Playlist ID'].isin(playlists_filtradas)]
    top_artist=filtered_df1.sort_values(by=["Count"], ascending=False).head(15)

    fig=plt.figure(figsize=(12, 22))
    ax=sns.barplot(
        x='Count',
        y='Artista',
        hue='Canción',
        data=top_artist,
        palette='viridis'
    )
    ax.set_title('Artistas')
    ax.set_xlabel('Número de Canciones')
    ax.set_ylabel('Artista')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=24)
    return st.pyplot(fig)  

def comparador_atributos_canciones(playlist_id1,playlist_id2,selected_song1,selected_song2):
    playlist_seleccionada1 = collect_data(playlist_id1)
    playlist_seleccionada2 = collect_data(playlist_id2)

    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    generos = ['pop', 'rock', 'hip hop', 'electronic', 'classical', 'jazz', 'country', 'latin']
    df_canciones1=predecir_genero_canciones(playlist_seleccionada1, client_id, client_secret, generos)
    df_canciones2=predecir_genero_canciones(playlist_seleccionada2, client_id, client_secret, generos)


    df_playlist_canciones = pd.concat([df_canciones1, df_canciones2], ignore_index=True)


    mean_features=['nombre','danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'instrumentalness', 'speechiness',
                      'popularidad', 'duración (segundos)']
    df_mean = df_playlist_canciones[mean_features]
    
    # Calcular medias por Playlist ID
    df = df_mean.groupby('nombre').mean().reset_index()
    filtered_df1 = df[df["nombre"].isin([selected_song1, selected_song2])]

    # Filtrar las playlists específicas
    # playlists_filtradas = [playlist_id1, playlist_id2]
    # df_filtrado = df[df['playlist'].isin(playlists_filtradas)]
    
    # Definir atributos para cada radar
    features_1 = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']
    features_2 = ['tempo', 'popularidad', 'duración (segundos)']
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=("Media de Atributos del Grupo 1", "Media de Atributos del Grupo 2"))
    
    valores_unicos = filtered_df1['nombre'].unique().tolist()
    for playlist_id in valores_unicos:
            # Filtrar datos para la playlist actual
            df_1 = filtered_df1[filtered_df1['nombre'] == playlist_id][features_1].mean()
            df_2 = filtered_df1[filtered_df1['nombre'] == playlist_id][features_2].mean()
            
            # Gráfico de radar para features_1
            fig.add_trace(go.Scatterpolar(
                r=df_1.values,
                theta=features_1,
                fill='toself',
                name=f'Canción {playlist_id} - Atributos 1'
            ), row=1, col=1)

            # Gráfico de radar para features_2
            fig.add_trace(go.Scatterpolar(
                r=df_2.values,
                theta=features_2,
                fill='toself',
                name=f'Canción {playlist_id} - Atributos 2'
            ), row=1, col=2)

        # Configurar el layout del gráfico
    fig.update_layout(
        template='plotly_dark',
        polar=dict(radialaxis=dict(visible=True)),
        title="Comparación de Atributos entre Canciones"
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
