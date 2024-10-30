import requests
import base64
import pandas as pd
#Definimos función para extraccion y adecuación de datos:
def collect_data(playlist_id):
    #Autenticacion
    
    client_id= "12f88fe9b7c14982bd0f03de6882817b"
    client_secret="58725b42fc634f12878f4dc8ac548ff4"
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
        print(f"Error al obtener token: {response.status_code}")
        print(response.text)
    
    
    # URL del endpoint para obtener la información de la playlist
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    # URL del endpoint para obtener la información de la playlist
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    audio_features_url = 'https://api.spotify.com/v1/audio-features/'

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
        playlist_data = []

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
            else:
                # En caso de fallo, usamos valores nulos para esos atributos
                danceability = energy = valence = tempo = acousticness = instrumentalness = speechiness = None

            # Añadir la información de la canción a la lista
            playlist_data.append({
                'Nombre': track_name,
                'Artistas': track_artists,
                'Duración (segundos)': track_duration,
                'Popularidad': track_popularity,
                'Explícito': track_explicit,
                'Fecha de Lanzamiento': track_release_date,
                'Danceability': danceability,
                'Energy': energy,
                'Valence': valence,
                'Tempo': tempo,
                'Acousticness': acousticness,
                'Instrumentalness': instrumentalness,
                'Speechiness': speechiness,
                "Playlist":playlist_info["name"],
                "Imagenes":playlist_info["images"][0]["url"]
            })

    else:
        print(f"Error al obtener la playlist: {response.status_code}")
        print(response.text)
        
    return pd.DataFrame(playlist_data)  # Crear un DataFrame con los datos
