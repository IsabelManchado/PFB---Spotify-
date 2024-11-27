import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
import streamlit as st

def clustering_canciones1(df):


    features = ['duración (segundos)', 'popularidad', 'danceability', 'energy', 'valence', 
                'tempo', 'acousticness', 'instrumentalness', 'speechiness',"explícito", "clave (key)","modo (mode)"]

   
    # Creamos el escalador (en este caso, StandardScaler)
    scaler = StandardScaler()

    # Escalamos los datos
    df_canciones_scaled = scaler.fit_transform(df[features])

    # Convertimos el resultado de la escala a un DataFrame para poder trabajar con él
    df_canciones_scaled = pd.DataFrame(df_canciones_scaled, columns=features)

    # Verificamos los primeros registros escalados
    #print(df_canciones_scaled.head())

    # Guardamos el objeto escalador en un archivo pickle
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    #print("Escalador guardado en el archivo 'scaler.pkl'.")
    # Cargar el DataFrame de las canciones y playlists
    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")

    # # Filtramos las canciones de una playlist específica
    # df_playlist_canciones = df_tracks[df_tracks['Playlist ID'] == playlist_id]

    # # Verificamos cuántas canciones tiene la playlist
    # #print(f"Número de canciones en la playlist {playlist_id}: {len(df_playlist_canciones)}")

    # # Obtener las canciones de la playlist
    # canciones_playlist = df_canciones[df_canciones['canción id'].isin(df_playlist_canciones['Canción ID'])]

    # Verificamos las canciones filtradas
    #print("Primeras canciones de la playlist filtrada:", canciones_playlist.head())

    # Seleccionamos las características numéricas que hemos escalado para el clustering
    X = df_canciones_scaled

    # Definimos el modelo de clustering KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)  # Usamos 3 clusters como ejemplo

    # Ajustamos el modelo
    kmeans.fit(X)

    # Añadimos las etiquetas de los clusters al DataFrame de canciones
    df['Cluster'] = kmeans.labels_

    plt.style.use("dark_background")
    
    with st.container():
        df=(df[['nombre', 'Cluster']])
        x = range(len(df)) 
        y = df['Cluster']
        fig, ax = plt.subplots()
        
        scatter= ax.scatter(x, y, c=y, cmap='viridis', edgecolor='k', s=100)
        ax.set_title("Distribución de Canciones por Clúster")
        ax.set_xlabel("Canción",fontsize=12)
        ax.set_ylabel("Clúster")
        ax.set_xticks(x, df['nombre'], rotation=90,fontsize=6)
        fig.colorbar(scatter, ax=ax, label='Cluster')
        st.pyplot(fig)
        st.markdown("Este gráfico muestra las canciones de la playlist asignadas a cada cluster.")
        st.divider()
    with st.container():
        fig, ax = plt.subplots()
        df1=(df["Cluster"].value_counts()).to_frame()

        colors = ['purple', 'yellow', 'aquamarine']
        ax.bar(df1.index.values, df1['count'], color=colors[:len(df1)], edgecolor='black')
        ax.set_title("Conteo de Canciones por Clúster")
        ax.set_xlabel("Clúster")
        ax.set_ylabel("Cantidad de Canciones")
        ax.set_xticks(df1.index.values)
        st.pyplot(fig)  
        st.markdown("Este gráfico muestra el número de canciones de la playlist asignadas a cada cluster.")
        st.divider()      
    with st.container():
        y_kmeans = kmeans.predict(X)

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        centroids = pca.transform(kmeans.cluster_centers_)
        # Gráfico de dispersión con colores para cada clúster y centroides
        fig, ax = plt.subplots()
        ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y_kmeans, s=50, cmap='viridis', vmin=0, vmax=2,)
        ax.scatter(centroids[:, 0], centroids[:, 1], s=200, c='red', marker='X', label='Centroids')
        ax.set_title(" Clústeres de Canciones")
        ax.legend()
        
    plt.tight_layout()
    

    return st.pyplot(fig)  

def clustering_playlist():
    scaler = StandardScaler()
    with open("scaler.pkl", "wb") as f:
            pickle.dump(scaler, f)

    # Unimos df_canciones con df_tracks para obtener las canciones de cada playlist
    df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
    df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    # Unimos los datos de las canciones con las playlists
    df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on="Canción ID", right_on="canción id")

    # Calculamos la media de las características numéricas para cada playlist
    playlist_features = ['duración (segundos)', 'popularidad', 'danceability', 'energy', 'valence', 
                        'tempo', 'acousticness', 'instrumentalness', 'speechiness',"explícito", "clave (key)","modo (mode)"]

    # Agrupamos por 'Playlist ID' y calculamos la media de cada característica
    df_playlist_stats = df_playlist_canciones.groupby('Playlist ID')[playlist_features].mean().reset_index()

    # Verificamos las nuevas características agregadas por playlist
    #print(df_playlist_stats.head())

    # Usamos el escalador previamente guardado para escalar las características de las playlists
    X_playlists_scaled = scaler.fit_transform(df_playlist_stats[playlist_features])

    # Verificamos que las características estén escaladas
    #print(X_playlists_scaled[:5])

    # Definimos el número de clusters (puedes ajustarlo según lo que necesites)
    kmeans_playlists = KMeans(n_clusters=4, random_state=42) 

    # Ajustamos el modelo de clustering
    kmeans_playlists.fit(X_playlists_scaled)

    y_kmeans = kmeans_playlists.predict(X_playlists_scaled)



    # Añadimos las etiquetas de los clusters al DataFrame de playlists
    df_playlist_stats['Cluster'] = kmeans_playlists.labels_

    plt.style.use("dark_background")
    
    with st.container():
        df=df_playlist_stats[['Playlist ID', 'Cluster']]

        x = range(len(df)) 
        y =y_kmeans
        fig, ax = plt.subplots()
        scatter2=ax.scatter(x, y, c=y, cmap='viridis', edgecolor='k', s=100)
        ax.set_title("Distribución de Playlist por Clúster")
        ax.set_xlabel("Playlist")
        ax.set_ylabel("Clúster")
        ax.set_xticks([])
        fig.colorbar(scatter2, ax=ax, label='Cluster')
        st.pyplot(fig)
        st.markdown("Este gráfico muestra las playlist asignadas a cada cluster.")
        st.divider()

    with st.container():
        fig, ax = plt.subplots()
        df1=(df_playlist_stats['Cluster'].value_counts()).to_frame()
        colors = ['mediumpurple', 'aquamarine', 'purple', 'yellow'] 

        ax.bar(df1.index.values, df1['count'], color=colors[:len(df1)], edgecolor='black')
        ax.set_title("Conteo de Playlist por Clúster")
        ax.set_xlabel("Clúster")
        ax.set_ylabel("Cantidad de Canciones")
        ax.set_xticks(df1.index.values)
        st.pyplot(fig)  
        st.markdown("Este gráfico muestra el número de playlist asignadas a cada cluster.")
        st.divider() 
    with st.container():
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_playlists_scaled)

        fig, ax = plt.subplots()
        ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y_kmeans, s=50, cmap='viridis', vmin='0', vmax='3',)
        centroids = pca.transform(kmeans_playlists.cluster_centers_)
        ax.scatter(centroids[:, 0], centroids[:, 1], s=200, c='red', marker='X', label='Centroids')
        ax.set_title("Gráfico de Dispersión con Clústeres de Playlist")
        ax.legend()
        
    plt.tight_layout()

    return st.pyplot(fig)