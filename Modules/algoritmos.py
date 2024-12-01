import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def algoritmo(playlist_usuario_id):
    # Cargar los datos
    playlists = pd.read_csv(r"..\PFB---Spotify-\EDA\playlists1.csv")  # Información general de las playlists
    canciones = pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")  # Características de las canciones
    tracks_playlists = pd.read_csv(r"..\PFB---Spotify-\EDA\tracks_playlists.csv")  # Relación entre playlists y canciones

    tracks_playlists_info = pd.merge(
    tracks_playlists, 
    canciones[['canción id', 'danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness','popularidad','duración (segundos)']], 
    left_on='Canción ID', 
    right_on='canción id', 
    how='inner'
)
    
    # Agrupar por 'Playlist ID' y calcular el promedio de las características acústicas
    playlist_features = tracks_playlists_info.groupby('Playlist ID')[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness','popularidad','duración (segundos)']].mean().reset_index()

    # Unir esta información con el DataFrame de playlists para obtener la información completa
    playlist_features = pd.merge(playlists, playlist_features, on='Playlist ID')



    # Obtener las canciones en esa playlist
    playlist_usuario_canciones = tracks_playlists_info[tracks_playlists_info['Playlist ID'] == playlist_usuario_id]

    # Promediamos las características de las canciones de esa playlist
    playlist_usuario_features = playlist_usuario_canciones[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness','popularidad','duración (segundos)']].mean().values.reshape(1, -1)

    # Extraer las características acústicas de todas las canciones
    canciones_features = canciones[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness','popularidad','duración (segundos)']]

    # Calcular la similitud entre la playlist del usuario y todas las canciones
    similitud_canciones = cosine_similarity(playlist_usuario_features, canciones_features)

    # Ordenar las canciones por similitud (de mayor a menor)
    indices_similares = similitud_canciones.argsort()[0][::-1]

    # Obtener las canciones más similares (por ejemplo, las 5 primeras)
    canciones_recomendadas = canciones.iloc[indices_similares[:5]]
    
    # Obtener las características acústicas de la playlist del usuario
    playlist_usuario_features = playlist_features[playlist_features['Playlist ID'] == playlist_usuario_id][['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness','popularidad','duración (segundos)']].values

    # Calcular la similitud del coseno entre la playlist del usuario y todas las playlists
    similitud_playlists = cosine_similarity(playlist_usuario_features, playlist_features[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness','popularidad','duración (segundos)']])

    # Ordenar las playlists por similitud (de mayor a menor)
    indices_similares_playlists = similitud_playlists.argsort()[0][::-1]

    # Obtener las playlists más similares (por ejemplo, las 5 primeras)
    playlists_recomendadas = playlist_features.iloc[indices_similares_playlists[:5]]



    return canciones_recomendadas, playlists_recomendadas
