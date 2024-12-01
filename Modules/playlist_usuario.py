import requests
import base64
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import streamlit as st

def collect_data(playlist_id):
    #Autenticacion
    
    client_id= "06c1d06e2e3149e7a07f5aba3b28961a"
    client_secret="c51a167e2e294337b5f80998a035b625"
    # URL para la autenticación
    auth_url = 'https://accounts.spotify.com/api/token'

    # Codifica el client_id y client_secret en base64
    client_credentials = f"{client_id}:{client_secret}"
    client_credentials_base64 = base64.b64encode(client_credentials.encode()).decode()

    # Cabeceras de la petición
    headers = {
        "Authorization": f"Basic {client_credentials_base64}",
    }

    # Datos del cuerpo de la petición (para obtener token con 'client_credentials')
    data = {
        "grant_type": "client_credentials"
    }

    # Hacer la petición POST para obtener el token
    response = requests.post(auth_url, headers=headers, data=data)

    # Verificar si la petición fue exitosa
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
    else:
        st.error(f"Error al obtener token: {response.status_code}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
    
    playlist_data = []
    # URL del endpoint para obtener la información de la playlist
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    # URL del endpoint para obtener la información de la playlist
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    audio_features_url = 'https://api.spotify.com/v1/audio-features/'
    img_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
    # Cabeceras de la petición (incluye el token de acceso)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Hacer la petición GET para obtener la información de la playlist
    response = requests.get(playlist_url, headers=headers)

    # Verificar si la petición fue exitosa
    if response.status_code == 200:
        playlist_info = response.json()

        # Obtener la lista de canciones (tracks)
        tracks = playlist_info['tracks']['items']

        # Crear una lista para almacenar los datos de las canciones
        

        # Recorrer las canciones y extraer la información
        for track_item in tracks:
            track = track_item['track']
            track_id = track['id']
            track_name = track['name']
            track_artists = ', '.join([artist['name'] for artist in track['artists']])
            track_duration = track['duration_ms'] / 1000  # Convertir duración de ms a segundos
            track_popularity = track['popularity']
            track_explicit = track['explicit']
            track_release_date = track['album']['release_date']
            track_url = track["external_urls"]["spotify"]
            track_imagen = track["album"]["images"][0]["url"] if track["album"]["images"] else None

            # Hacer la petición GET para obtener las características de audio de cada canción
            audio_features_response = requests.get(audio_features_url + track_id, headers=headers)

            if audio_features_response.status_code == 200:
                audio_features = audio_features_response.json()
                danceability = audio_features['danceability']
                energy = audio_features['energy']
                valence = audio_features['valence']
                tempo = audio_features['tempo']
                acousticness = audio_features['acousticness']
                instrumentalness = audio_features['instrumentalness']
                speechiness = audio_features['speechiness']
                clave = audio_features['key']
                modo = audio_features['mode'] 
            else:
                # En caso de fallo, usamos valores nulos para esos atributos
                danceability = energy = valence = tempo = acousticness = instrumentalness = speechiness = clave = modo = None
            
            imagen_playlist = requests.get(img_url, headers=headers)
            if imagen_playlist.status_code == 200:
                imag_playlist = imagen_playlist.json()
                track_imagen=imag_playlist[0]["url"]

            # Añadir la información de la canción a la lista
            playlist_data.append({
                'Canción ID': track_id,
                'Nombre': track_name,
                'Artistas': track_artists,
                'Duración (segundos)': track_duration,
                'Popularidad': track_popularity,
                'Explícito': track_explicit,
                'Fecha de Lanzamiento': track_release_date,
                'Url de Spotify': track_url,
                'Imagen': track_imagen,
                'Danceability': danceability,
                'Energy': energy,
                'Valence': valence,
                'Tempo': tempo,
                'Acousticness': acousticness,
                'Instrumentalness': instrumentalness,
                'Speechiness': speechiness,
                "Playlist":playlist_info["name"],
                'Clave (Key)': clave,
                'Modo (Mode)': modo
                
            })

    else:
        st.error(f"Error al obtener la playlist: {response.status_code}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
        
    return pd.DataFrame(playlist_data)  # Crear un DataFrame con los datos


def predecir_genero_canciones(df_canciones, client_id, client_secret, generos):
    # Autenticación con Spotify
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Función interna para obtener canciones de un género
    def obtener_canciones_de_genero(genre, num_playlists=10, num_tracks=50):
        playlists = sp.search(q=genre, type='playlist', limit=num_playlists)
        tracks = []
        for playlist in playlists['playlists']['items']:
            playlist_uri = playlist['uri']
            playlist_tracks = sp.playlist_tracks(playlist_uri)
            for item in playlist_tracks['items']:
                if item['track']:
                    tracks.append(item['track']['id'])
                if len(tracks) >= num_tracks:
                    break
            if len(tracks) >= num_tracks:
                break
        return tracks

    # Función interna para obtener características de canciones
    def obtener_caracteristicas_canciones(track_ids):
        features = sp.audio_features(track_ids)
        return features

    # Calcular promedios de características por género
    genero_promedios = {}
    for genero in generos:
        track_ids = obtener_canciones_de_genero(genero)
        features = obtener_caracteristicas_canciones(track_ids)
        danceability, energy, valence, acousticness, tempo = [], [], [], [], []
        for feature in features:
            if feature:
                danceability.append(feature['danceability'])
                energy.append(feature['energy'])
                valence.append(feature['valence'])
                acousticness.append(feature['acousticness'])
                tempo.append(feature['tempo'])
        genero_promedios[genero] = {
            'danceability': np.mean(danceability),
            'energy': np.mean(energy),
            'valence': np.mean(valence),
            'acousticness': np.mean(acousticness),
            'tempo': np.mean(tempo)
        }

    # Crear DataFrame de promedios
    genero_promedios_df = pd.DataFrame(genero_promedios).T

    # Escalar los datos de géneros
    scaler = StandardScaler()
    X_generos_scaled = scaler.fit_transform(genero_promedios_df)
    y_generos = genero_promedios_df.index

    # Entrenar modelo Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_generos_scaled, y_generos)

    # Predecir géneros en df_canciones
    df_canciones.columns = df_canciones.columns.str.lower()
    caracteristicas = ['danceability', 'energy', 'valence', 'acousticness', 'tempo']

    if all(col in df_canciones.columns for col in caracteristicas):
        X_canciones_scaled = scaler.transform(df_canciones[caracteristicas])
        df_canciones['predicted_genre'] = rf.predict(X_canciones_scaled)
    else:
        raise ValueError("Faltan algunas columnas necesarias en df_canciones.")
    
    return df_canciones


def clustering_canciones1(playlist_id):

    # Seleccionamos las características de las canciones que quieres escalar
    # Por ejemplo, algunas características numéricas como: 'duración (segundos)', 'popularidad', etc.
    features = ['duración (segundos)', 'popularidad', 'danceability', 'energy', 'valence', 
                'tempo', 'acousticness', 'instrumentalness', 'speechiness',"explícito", "clave (key)","modo (mode)"]

    # Cargamos el DataFrame df_canciones
    df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    # Creamos el escalador (en este caso, StandardScaler)
    scaler = StandardScaler()

    # Escalamos los datos
    df_canciones_scaled = scaler.fit_transform(playlist_seleccionada[features])

    # Convertimos el resultado de la escala a un DataFrame para poder trabajar con él
    df_canciones_scaled = pd.DataFrame(df_canciones_scaled, columns=features)

    # Verificamos los primeros registros escalados
    #print(df_canciones_scaled.head())

    # Guardamos el objeto escalador en un archivo pickle
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    #print("Escalador guardado en el archivo 'scaler.pkl'.")

    features = ['duración (segundos)', 'popularidad', 'danceability', 'energy', 'valence', 
                'tempo', 'acousticness', 'instrumentalness', 'speechiness',"explícito", "clave (key)","modo (mode)"]

    # Cargamos el DataFrame df_canciones
    df_canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")

    # Creamos el escalador (en este caso, StandardScaler)
    scaler = StandardScaler()

    # Escalamos los datos
    df_canciones_scaled = scaler.fit_transform(df_canciones[features])

    # Convertimos el resultado de la escala a un DataFrame para poder trabajar con él
    df_canciones_scaled = pd.DataFrame(df_canciones_scaled, columns=features)

    # Verificamos los primeros registros escalados
    #print(df_canciones_scaled.head())

    # Guardamos el objeto escalador en un archivo pickle
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    #print("Escalador guardado en el archivo 'scaler.pkl'.")
    # Cargar el DataFrame de las canciones y playlists
    df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")

    # Filtramos las canciones de una playlist específica
    df_playlist_canciones = df_tracks[df_tracks['Playlist ID'] == playlist_id]

    # Verificamos cuántas canciones tiene la playlist
    #print(f"Número de canciones en la playlist {playlist_id}: {len(df_playlist_canciones)}")

    # Obtener las canciones de la playlist
    canciones_playlist = df_canciones[df_canciones['canción id'].isin(df_playlist_canciones['Canción ID'])]

    # Verificamos las canciones filtradas
    #print("Primeras canciones de la playlist filtrada:", canciones_playlist.head())

    # Seleccionamos las características numéricas que hemos escalado para el clustering
    X = df_canciones_scaled.loc[canciones_playlist.index, features]

    # Definimos el modelo de clustering KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)  # Usamos 3 clusters como ejemplo

    # Ajustamos el modelo
    kmeans.fit(X)

    # Añadimos las etiquetas de los clusters al DataFrame de canciones
    canciones_playlist['Cluster'] = kmeans.labels_

    plt.style.use("dark_background")
    
    with st.container():
        df=(canciones_playlist[['nombre', 'Cluster']])
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
        df1=(canciones_playlist["Cluster"].value_counts()).to_frame()

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