import streamlit as st

# Título de la app
st.title("Cómo y por qué")
st.write("Sección técnica que indica la metodología del desarrollo")

# Mostrar ETL Python con explicación
with st.expander("ETL desde la API de Spotify"):
    st.write("La API permite a los desarrolladores acceder a información detallada sobre canciones, artistas, álbumes, playlists, y más. Ofrece una gran variedad de endpoints que permiten extraer datos útiles para análisis de música, creación de recomendadores y otras aplicaciones musicales.")
    st.write("Para interactuar con la API, se requiere:")
    st.write("- Autenticación: Se utiliza un OAuth token que puede obtenerse registrando una aplicación en el Spotify for Developers Dashboard.")
    st.write("- Rate Limits: Spotify impone límites en la cantidad de solicitudes que se pueden realizar por minuto.")
    st.write("")
    st.write("Para obtener el token lo que haremos es usar el client_id y client_secret y codificarlos en base64.")
    st.write("La codificación en Base64 es una técnica comúnmente utilizada en el manejo de datos binarios y en la transmisión de información a través de medios que manejan texto, como HTTP. En el contexto de la autenticación con la API de Spotify, se utiliza para codificar las credenciales del cliente (es decir, el client_id y el client_secret) cuando se solicita un token de acceso.")
    st.code("""
# Herramientas
import requests
import base64

# Credenciales de Spotify
client_id = "inserte aquí su client_id"
client_secret = "inserte aquí su client_secret"

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
    print("Token de acceso obtenido:", access_token)
else:
    print(f"Error al obtener token: {response.status_code}")
    print(response.text)

access_token = 'access_token generado'
    """, language = "python")

    st.write("Una vez hayamos obtenido el token lo primero que haremos es desarrollar una script para obtener la informacion de una canción.")
    st.write("Para obtener la ID de una canción lo que debemos hacer es ir a la canción que queramos y darle a los 3 puntos y copiar el enlace que nos pone, por ejemplo: https://open.spotify.com/intl-es/track/6mnfGyPzbzSe8olYGM44pU?si=6e3cf8d12af84d38")
    st.write("Y para obtener la id que necesitamos lo que haremos es quedarnos con el código que hay despues de /track/ y antes de ?si= es decir, quedaría así: 6mnfGyPzbzSe8olYGM44pU")
    st.write("Con este script obtendremos lo que sería la informacion básica de una canción.")
    st.code("""
# Herramientas.
import requests

# ID de la canción que quieres consultar (puedes obtener esto desde la app de Spotify)
track_id = '6mnfGyPzbzSe8olYGM44pU'  # Ejemplo: canción Luna llena - Beny Jr

# URL del endpoint para obtener información de la canción
track_url = f'https://api.spotify.com/v1/tracks/{track_id}'

# Cabeceras de la petición (incluye el token de acceso)
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Hacer la petición GET para obtener la información de la canción
response = requests.get(track_url, headers=headers)

# Verificar si la petición fue exitosa
if response.status_code == 200:
    track_info = response.json()
    print("Información de la canción:")
    print(f"Nombre: {track_info['name']}")
    print(f"Artista(s): {[artist['name'] for artist in track_info['artists']]}")
    print(f"Álbum: {track_info['album']['name']}")
    print(f"Popularidad: {track_info['popularity']}")
    print(f"Duración (ms): {track_info['duration_ms']}")
else:
    print(f"Error al obtener la canción: {response.status_code}")
    print(response.text)
    """, language = "python")

    st.write("Ahora lo que queremos hacer es obtener la información de una playlist y que nos saque la información de cada canción de esa playlist. Para ello tendremos que usar el mismo método de la ID, pero esta vez de la playlist, que se obtiene igual que hemos comentado anteriormente.")
    st.write("Con este script obtendremos lo que sería la informacion básica de las canciones de la playlist que hayamos elegido")
    st.code("""
# Herramientas.
import requests

# ID de la playlist que quieres consultar (puedes obtener esto desde la app de Spotify)
playlist_id = '37i9dQZF1DWUH2AzNQzWua'  # Ejemplo: playlist "Top 50 - Spain"

# URL del endpoint para obtener la información de la playlist
playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'

# Cabeceras de la petición (incluye el token de acceso)
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Hacer la petición GET para obtener la información de la playlist
response = requests.get(playlist_url, headers=headers)

# Verificar si la petición fue exitosa
if response.status_code == 200:
    playlist_info = response.json()

    # Imprimir algunos detalles básicos de la playlist
    print(f"Nombre de la playlist: {playlist_info['name']}")
    print(f"Descripción: {playlist_info['description']}")
    print(f"Número de canciones: {playlist_info['tracks']['total']}")

    # Obtener la lista de canciones (tracks)
    tracks = playlist_info['tracks']['items']
    
    # Recorrer las canciones y extraer la información
    print("\nCanciones en la playlist:")
    for i, track_item in enumerate(tracks, start=1):
        track = track_item['track']
        track_name = track['name']
        track_artists = ', '.join([artist['name'] for artist in track['artists']])
        track_duration = track['duration_ms'] / 1000  # Convertir duración de ms a segundos
        
        print(f"{i}. {track_name} - {track_artists} ({track_duration} segundos)")
else:
    print(f"Error al obtener la playlist: {response.status_code}")
    print(response.text)
    """, language = "python")            

    st.write("Ahora el objetivo que tenemos es crear un DataFrame con la informacion que creemos que puede ser de utilidad.")
    st.code("""
# Herramientas
import requests
import pandas as pd

# ID de la playlist que quieres consultar 
playlist_id = '37i9dQZF1DWUH2AzNQzWua' 

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
            'Speechiness': speechiness
        })

    # Crear un DataFrame con los datos
    df = pd.DataFrame(playlist_data)

else:
    print(f"Error al obtener la playlist: {response.status_code}")
    print(response.text)
    """, language = "python")

    st.write("Ahora lo que haremos es limpiar lo que son los Datos, aunque viendo la calidad de los datos con los que trabaja Spotify, modificaremos pocas cosas.")
    st.code("""
# Herramientas
import pandas as pd

# Cargar los datos desde el CSV generado
df = pd.read_csv('playlist_info_con_audio_features.csv')

# A) Eliminar filas con valores nulos en las características de audio
df_cleaned = df.dropna(subset=['Danceability', 'Energy', 'Valence', 'Tempo', 'Acousticness', 'Instrumentalness', 'Speechiness'])

# B) Convertir la columna 'Fecha de Lanzamiento' en tipo datetime
df_cleaned['Fecha de Lanzamiento'] = pd.to_datetime(df_cleaned['Fecha de Lanzamiento'], errors='coerce')

# C) Eliminar duplicados (si existen)
df_cleaned = df_cleaned.drop_duplicates(subset=['Nombre', 'Artistas'], keep='first')
    """, language = "python")

    st.write("Una vez limpios los guardaremos en un csv.")
    st.code("""
# Guardar los datos limpios en un nuevo CSV
df_cleaned.to_csv('playlist.csv', index=False)
    """, language = "python")

    st.write("Nuestro objetivo ahora sera crear 3 dataframes los cuales tengan relación.")
    st.write("Lo primero que haremos será crear un df con 1200 playlists que nos diga el nombre de la playlist, la descripción, elñ número de canciones que contiene la playlist y la URL.")
    st.code("""
# Herramientas
import requests
import pandas as pd
import time

# Acceso a la API de Spotify (reemplaza 'access_token' por tu token válido)
  # Reemplaza con tu token real
headers = {
    "Authorization": f"Bearer {access_token}"
}

# URL de búsqueda de la API de Spotify
search_url = 'https://api.spotify.com/v1/search'

# Función para buscar playlists con un término específico y almacenar los resultados
def search_playlists(query, headers, limit=50, offset=0):
    params = {
        'q': query,
        'type': 'playlist',
        'limit': limit,
        'offset': offset
    }
    
    # Petición GET a la API de Spotify
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code == 200:
        search_results = response.json()
        playlists = search_results['playlists']['items']
        
        # Extraer y devolver la información de las playlists
        return [{
            'Playlist ID': playlist['id'],
            'Nombre Playlist': playlist['name'],
            'Descripción': playlist['description'],
            'Número de canciones': playlist['tracks']['total'],
            'Url de Spotify': playlist['external_urls']['spotify']
        } for playlist in playlists]
    else:
        print(f"Error en la búsqueda de playlists: {response.status_code}")
        print(response.text)
        return []

# Lista para almacenar los datos de playlists
all_playlists_data = []

# Términos de búsqueda para obtener diversidad en los resultados
search_terms = ["Top", "Hits", "Pop", "Rock", "Mood", "Workout"]  
limit = 50  # Número máximo de playlists por búsqueda
offset = 0  # Empezar desde el primer resultado

# Loop para obtener al menos 2000 playlists
for term in search_terms:
    while len(all_playlists_data) < 1200:
        # Obtener datos de playlists para el término de búsqueda actual
        playlists = search_playlists(term, headers, limit=limit, offset=offset)
        
        # Añadir playlists al listado general, asegurando que sean únicas
        all_playlists_data.extend(playlists)
        
        # Incrementar el offset para la siguiente página de resultados
        offset += limit
        
        # Si no hay más playlists, pasamos al siguiente término de búsqueda
        if not playlists:
            break
        
        # Pausa para no sobrecargar la API
        time.sleep(0.1)
    
    # Restablecer el offset para el siguiente término de búsqueda
    offset = 0

    # Si ya alcanzamos las 2000 playlists, salimos del loop
    if len(all_playlists_data) >= 1200:
        break

# Crear DataFrame con los datos de todas las playlists
playlists1 = pd.DataFrame(all_playlists_data[:1200])  # Limitar a las primeras 2000 playlists

# Mostrar el DataFrame
print("DataFrame de Playlists:")
print(playlists1.head())
print(f"\nTotal de playlists recopiladas: {len(playlists1)}")
            
# Guardamos en un csv.
playlists1.to_csv("playlists1.csv", index=False)
    """, language = "python")

    st.write("Una vez tengamos el df de las playlist, ahora lo que haremos será crear otro que contenga las ID's de las playlists y las ID's de las canciones de cada playlist.")
    st.write("Nuestro objetivo con esto será que gracias a esto podremos ver si una cancion está en una o varias playlist y luego será mas fácil a la hora de extraer la informacion de cada canción.")
    st.code("""
# Herramientas
import requests
import pandas as pd
import time

# Función para obtener las canciones de una playlist y sus características de audio
def get_playlist_tracks(playlist_id, headers):
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    # Petición para obtener los datos de la playlist
    response = requests.get(playlist_url, headers=headers)

    if response.status_code == 200:
        playlist_info = response.json()
        
        # Lista para almacenar los datos de cada canción
        tracks_data = []

        # Obtener las canciones de la playlist
        tracks = playlist_info['tracks']['items']
        for track_item in tracks:
            track = track_item['track']

            # Verificar si track es None
            if track is None:
                continue

            track_id = track['id']

            # Detalles de la canción
            tracks_data.append({
                'Canción ID': track_id,
                'Playlist ID': playlist_id
            })

        return tracks_data
    else:
        print(f"Error al obtener la playlist: {response.status_code}")
        print(response.text)
        return []

# Acceso a la API de Spotify (reemplaza 'access_token' por tu token válido)
access_token   # Reemplaza con tu token real
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Obtener los IDs de las playlists desde el DataFrame existente
playlist_ids = playlists1['Playlist ID'].tolist()  # Asegúrate de que df_playlists está definido

# Listas para almacenar los datos de las canciones y sus playlists
all_tracks_playlist_data = []

# Recorrer cada playlist y extraer los datos de las canciones
for playlist_id in playlist_ids:
    tracks_data = get_playlist_tracks(playlist_id, headers)
    all_tracks_playlist_data.extend(tracks_data)

    # Pausa para evitar sobrecargar la API
    time.sleep(0.1)

# Crear DataFrame con los datos de las canciones y sus playlists
tracks_playlists1 = pd.DataFrame(all_tracks_playlist_data)

# Mostrar el DataFrame
print("DataFrame de Canciones y Playlists:")
print(tracks_playlists1.head())
print(f"\nTotal de registros en el DataFrame: {len(tracks_playlists1)}")
            
# Pequeño ETL
# Obtener valores únicos de la columna 'Playlist ID'
unique_playlist_ids = tracks_playlists1['Playlist ID'].unique()

# Obtener valores únicos de la columna 'Canción ID'
unique_track_ids = tracks_playlists1['Canción ID'].unique()

# Contar la cantidad de valores únicos
num_unique_playlists = len(unique_playlist_ids)
num_unique_tracks = len(unique_track_ids)

print(f"\nNúmero de Playlist IDs únicos: {num_unique_playlists}")
print(f"Número de Canción IDs únicos: {num_unique_tracks}")

# Guardamos el resultado en un csv.
tracks_playlists1.to_csv("tracks_playlists.csv", index=False)
    """, language = "python")

    st.write("Codigo para extraer la informacion de las canciones del df de ID's usando .unique().")
    st.write("Antes que nada eliminaremos las ID de las canciones que sean None.")
    st.code("""
tracks_playlists1 = tracks_playlists1.dropna()
    """, language = "python")

    st.write("Y extraemos la informacion.")
    st.code("""
# Herramientas
import requests
import pandas as pd
import time
import base64
from datetime import datetime

# Función para obtener el token de acceso
def obtener_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error al obtener token: {response.status_code}")
        return None

# Función para obtener datos de canciones en un lote
def obtener_datos_cancion(batch, access_token):
    # URL de la API de Spotify para obtener datos de múltiples canciones
    url_tracks = f"https://api.spotify.com/v1/tracks"
    url_audio_features = f"https://api.spotify.com/v1/audio-features"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Convertir lista de IDs en un solo string separado por comas
    track_ids_str = ",".join(batch)

    # Obtener datos de pistas
    response_tracks = requests.get(f"{url_tracks}?ids={track_ids_str}", headers=headers)
    response_audio_features = requests.get(f"{url_audio_features}?ids={track_ids_str}", headers=headers)

    # Comprobar si las solicitudes fueron exitosas
    if response_tracks.status_code == 200 and response_audio_features.status_code == 200:
        tracks = response_tracks.json()["tracks"]
        audio_features_list = response_audio_features.json()["audio_features"]

        datos_canciones = []
        for track, audio_features in zip(tracks, audio_features_list):
            if track and audio_features:
                datos_cancion = {
                    "Canción ID": track["id"],
                    "Nombre": track["name"],
                    "Artistas": ", ".join([artist["name"] for artist in track["artists"] if artist["name"] is not None]),
                    "Duración (segundos)": track["duration_ms"] / 1000,
                    "Popularidad": track["popularity"],
                    "Explícito": track["explicit"],
                    "Fecha de Lanzamiento": track["album"]["release_date"],
                    "Url de Spotify": track["external_urls"]["spotify"],
                    "Imagen": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                    "Danceability": audio_features.get("danceability"),
                    "Energy": audio_features.get("energy"),
                    "Valence": audio_features.get("valence"),
                    "Tempo": audio_features.get("tempo"),
                    "Acousticness": audio_features.get("acousticness"),
                    "Instrumentalness": audio_features.get("instrumentalness"),
                    "Speechiness": audio_features.get("speechiness"),
                    "Clave (Key)": audio_features.get("key"),
                    "Modo (Mode)": audio_features.get("mode")
                }
                datos_canciones.append(datos_cancion)
        return datos_canciones
    elif response_tracks.status_code == 429 or response_audio_features.status_code == 429:
        retry_after = int(response_tracks.headers.get("Retry-After", 2))
        print(f"Límite de velocidad alcanzado. Esperando {retry_after} segundos...")
        time.sleep(retry_after)
        return obtener_datos_cancion(batch, access_token)
    else:
        print(f"Error al obtener datos para el lote: {response_tracks.status_code}, {response_audio_features.status_code}")
        return None

# Lista de IDs de canciones
track_ids = tracks_playlists1["Canción ID"].unique()

# Inicializar DataFrame y temporizador
df_canciones = pd.DataFrame(columns=[
    "Canción ID", "Nombre", "Artistas", "Duración (segundos)", "Popularidad", "Explícito", "Fecha de Lanzamiento", 
    "Url de Spotify", "Imagen", "Danceability", "Energy", "Valence", "Tempo", "Acousticness", 
    "Instrumentalness", "Speechiness", "Clave (Key)", "Modo (Mode)"
])

client_id = "10d944ee7fad41d9aa6b0e04a09a96c4"
client_secret = "d5db29896c074e95b7ae73777feadb79"
access_token = obtener_token(client_id, client_secret)

if access_token:
    for i in range(0, len(track_ids), 50):  # Procesar en lotes de 50 IDs
        batch = track_ids[i:i + 50]  # Extraer un lote de hasta 50 IDs
        datos = obtener_datos_cancion(batch, access_token)

        if datos:
            df_canciones = pd.concat([df_canciones, pd.DataFrame(datos)], ignore_index=True)
            df_canciones.to_csv("datos_canciones.csv", index=False)

        # Pausa para evitar el límite de velocidad
        time.sleep(1.0)  # 1 segundo para evitar problemas con el límite de velocidad
    
    print(df_canciones)
else:
    print("No se pudo obtener el token de acceso.")
    """, language = "python")

    st.write("Con esto finalizamos la extracción, transformación y carga de la información obtenida desde la API. Base fundamental para desarrollar éste proyecto")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### Soy un separador ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

# Clusters
with st.expander("Creación de Clusters"):
    st.write("Análisis y Clustering de Canciones")
    st.write("1. Importación de bibliotecas y carga de datos")
    st.write("- Se cargan los datos de canciones, playlists y la relación entre ambas. Se ajusta la columna explícito para asegurar que sea numérica.")
    st.code("""
# Herramientas
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

# Eliminamos warnings innecesarios
import warnings
warnings.filterwarnings('ignore')

# Carga de los datos
df_canciones = pd.read_csv("canciones_total.csv")
df_playlists = pd.read_csv("playlists1.csv")
df_tracks = pd.read_csv("tracks_playlists.csv")

# Conversión del campo 'explícito' a entero
df_canciones['explícito'] = df_canciones['explícito'].astype(int)
    """, language = "python")
    st.write("2. Selección y escalado de características")
    st.write("- Se escalan las características seleccionadas para estandarizar su rango. El escalador se guarda para su reutilización.")
    st.code("""
# Selección de características numéricas relevantes
features = ['duración (segundos)', 'danceability', 'energy', 'valence', 
            'tempo', 'acousticness', 'instrumentalness', 'speechiness', "explícito", "clave (key)", "modo (mode)"]

# Escalado de datos
scaler = StandardScaler()
df_canciones_scaled = scaler.fit_transform(df_canciones[features])
df_canciones_scaled = pd.DataFrame(df_canciones_scaled, columns = features)

# Primeros registros escalados
print(df_canciones_scaled.head())
print('')

# Guardar el escalador
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Escalador guardado en el archivo 'scaler.pkl'.")
print('')
    """, language = "python")
    st.write("3. Clustering de canciones en una playlist específica")
    st.write("- Se filtran las canciones de una playlist y se agrupan en clusters usando K-Means.")
    st.code("""
# Filtrar canciones de una playlist específica
playlist_id = '37i9dQZEVXbMDoHDwVN2tF'
df_playlist_canciones = df_tracks[df_tracks['Playlist ID'] == playlist_id]
canciones_playlist = df_canciones[df_canciones['canción id'].isin(df_playlist_canciones['Canción ID'])]

# Verificamos cuántas canciones tiene la playlist
print(f"Número de canciones en la playlist {playlist_id}: {len(canciones_playlist)}")
print('')

# Realizar clustering con DBSCAN
X = df_canciones_scaled.loc[canciones_playlist.index, features]
dbscan = DBSCAN(eps=2.66, min_samples=3)
clusters = dbscan.fit_predict(X)


# Asignar clusters al DataFrame
canciones_playlist['Cluster'] = clusters

# Verificar los clusters generados
print("Distribución de clusters generados por DBSCAN:")
print(canciones_playlist['Cluster'].value_counts())
print('')

# Verificar las primeras canciones con su cluster asignado
print("Primeras canciones de la playlist con clusters asignados:")
print(canciones_playlist[['nombre', 'Cluster']].head())
print('')
    """, language = "python")
    st.write("NearestNeighbors")
    st.code("""
# Damos valor deseado a K
k = 3  

# Calcular las distancias a los K vecinos más cercanos
neighbors = NearestNeighbors(n_neighbors=k)
neighbors_fit = neighbors.fit(X)
distances, indices = neighbors_fit.kneighbors(X)

# Ordenar las distancias
distances = np.sort(distances[:, k-1], axis=0)

# Graficar el gráfico de distancias
plt.plot(distances)
plt.xlabel('Número de puntos')
plt.ylabel(f'Distancia al {k}-ésimo vecino más cercano')
plt.title('Gráfico de distancias K-Vecinos más Cercanos')
plt.show()
    """, language = "python")
    st.write("Análisis y Clustering de Playlists")
    st.write("1. Unión de Canciones y Playlists")
    st.write("- Se combinan los datos de canciones (df_canciones) y playlists (df_tracks) para vincular las canciones con sus respectivas playlists")
    st.code("""
df_playlist_canciones = pd.merge(df_tracks, df_canciones, left_on = "Canción ID", right_on = "canción id")
    """, language = "python")
    st.write("2. Cálculo de Estadísticas por Playlist")
    st.write("- Se agrupan las canciones por Playlist ID y se calculan las medias de las características numéricas seleccionadas")
    st.code("""
playlist_features = ['duración (segundos)', 'danceability', 'energy', 'valence', 
                     'tempo', 'acousticness', 'instrumentalness', 'speechiness', "explícito", 
                     "clave (key)", "modo (mode)"]

df_playlist_stats = df_playlist_canciones.groupby('Playlist ID')[playlist_features].mean().reset_index()
    """, language = "python")
    st.write("3. Escalado de Datos")
    st.write("- Se utiliza el mismo escalador previamente guardado (scaler.pkl) para normalizar las características de las playlists")
    st.code("""
X_playlists_scaled = scaler.fit_transform(df_playlist_stats[playlist_features])
    """, language = "python")
    st.write("4. Clustering de Playlists")
    st.write("- Se agrupan las playlists en 4 clusters utilizando KMeans")
    st.code("""
dbscan = DBSCAN(eps=2.758, min_samples= 5)  
df_playlist_stats['Cluster'] = dbscan.fit_predict(X_playlists_scaled)

# 3. Verificar la cantidad de clusters formados
print(df_playlist_stats['Cluster'].value_counts())  # Imprime la cantidad de playlists en cada cluster

# 4. Visualización (si quieres graficar el clustering en 2D usando PCA para reducir dimensiones)
from sklearn.decomposition import PCA

# Reducimos la dimensionalidad a 2 componentes para visualización
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_playlists_scaled)

# Graficamos el clustering
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df_playlist_stats['Cluster'], cmap='viridis')
plt.title('Clustering de Playlists con DBSCAN')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.colorbar(label='Cluster')
plt.show()
            
# Guardamos nuevo CSV con clusters
df_playlist_stats.to_csv('df_cluster_playlist.csv', index = False)
    """, language = "python")
    st.write("5. Visualización y validación")
    st.code("""
# Selección de k vecinos más cercanos
k = 5  

# Calcular las distancias a los k vecinos más cercanos
neighbors = NearestNeighbors(n_neighbors=k)
neighbors_fit = neighbors.fit(X_playlists_scaled)
distances, indices = neighbors_fit.kneighbors(X_playlists_scaled)

# Ordenar las distancias al k-ésimo vecino más cercano
distances = np.sort(distances[:, k-1], axis=0)

# Graficar el gráfico de distancias
plt.figure(figsize=(10, 6))
plt.plot(distances)
plt.xlabel('Número de puntos')
plt.ylabel(f'Distancia al {k}-ésimo vecino más cercano')
plt.title('Gráfico de distancias K-Vecinos más Cercanos')
plt.grid(True)
plt.show()
    """, language = "python")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### Soy un separador ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

with st.expander("Modelado"):
    st.write("Herramientas + Comprender & preparar los datos")
    st.code("""
# Carga y manejo de datos
import pandas as pd
import numpy as np

# Escalado y preprocesamiento
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Clustering
from sklearn.cluster import KMeans

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns

# Reducción de dimensionalidad
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Almacenamiento de modelos
import pickle

# Cargar los datos
df_canciones = pd.read_csv("df_cluster_canciones.csv")
df_tracks = pd.read_csv("df_cluster_playlist.csv")

# Eliminar duplicados
df_canciones = df_canciones.drop_duplicates()
    """, language = "python")

    st.write("1. Análisis exploratorio post-clustering")
    st.write("Canciones (df_canciones)")
    st.code("""
# Seleccionar columnas numéricas
numeric_columns = df_canciones.select_dtypes(include=['number']).columns

# Verificar si hay valores no válidos en las columnas numéricas
for col in numeric_columns:
    print(f"Columna: {col}")
    print(df_canciones[col].unique())
    print("")  # Espacio para mejorar legibilidad

# Intentar convertir a numérico, reemplazando valores no válidos con NaN
for col in numeric_columns:
    df_canciones[col] = pd.to_numeric(df_canciones[col], errors='coerce')

# Revisar si hay valores NaN después de la conversión
print(df_canciones[numeric_columns].isnull().sum())

# Reemplazar valores NaN con la media de la columna
df_canciones[numeric_columns] = df_canciones[numeric_columns].fillna(df_canciones[numeric_columns].mean())

# Agrupar por 'Cluster' y calcular la media solo para las columnas numéricas
cluster_stats_canciones = df_canciones.groupby('Cluster')[numeric_columns].mean()
print(cluster_stats_canciones)

print('') # Espacio en respuesta
    """, language = "python")

    st.write("Visualizazción de los clusters")
    st.code("""
# Visualización de los clusters
pca = PCA(n_components = 2)
pca_result = pca.fit_transform(df_canciones[numeric_columns])

plt.figure(figsize = (15, 5))
plt.scatter(pca_result[:, 0], pca_result[:, 1], c = df_canciones['Cluster'], cmap = 'viridis', alpha = 0.7)
plt.colorbar(label = 'Cluster')
plt.title('Visualización de Clusters con PCA')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
    """, language = "python")

    st.write("Canciones por cluster")
    st.code("""
# Distribución de canciones por cluster en las playlists
plt.figure(figsize = (15, 5))
df_tracks['Cluster'].value_counts().plot(kind = 'pie', autopct = '%1.1f%%', colors = sns.color_palette('Set1', n_colors = 4))
plt.title('Distribución de canciones por cluster en las playlists', fontsize = 16)
plt.ylabel('')
plt.show()
            
# Validación del clustering
score = silhouette_score(df_canciones[numeric_columns], df_canciones['Cluster'])
print(f'Silhouette Score: {score}')
            
# Guardamos CSV
df_canciones.to_csv('canciones_clusterizadas.csv', index = False)
    """, language = "python")

    st.write("Recomendación de canciones")
    st.code("""
# Recomendación de canciones.
def recomendar_canciones(cancion_id, df, n=5):
    cluster_id = df.loc[cancion_id, 'Cluster']
    canciones_similares = df[df['Cluster'] == cluster_id].sample(n)
    return canciones_similares[['nombre', 'artistas']]

recomendaciones = recomendar_canciones(cancion_id = 0, df = df_canciones)
print(recomendaciones)
    """, language = "python")

    st.write("Otros modelados para canciones")
    st.write("Modelado predictivo")
    st.code("""
# Selección de columnas numéricas relevantes para clustering
numeric_columns_canciones = ['duración (segundos)', 'danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']

# Definir las características y la variable objetivo
X = df_canciones[numeric_columns_canciones]
y = df_canciones['popularidad']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de regresión lineal
model_lr = LinearRegression()

# Ajustar el modelo
model_lr.fit(X_train, y_train)

# Predecir sobre los datos de prueba
y_pred = model_lr.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error (MSE) de la regresión lineal: {mse}')
    """, language = "python")

    st.write("Random Forest Regressor para popularidad")
    st.code("""
# Crear el modelo RandomForestRegressor
model_rf = RandomForestRegressor(n_estimators = 100, random_state = 42)

# Ajustar el modelo
model_rf.fit(X_train, y_train)

# Predecir sobre los datos de prueba
y_pred_rf = model_rf.predict(X_test)

# Evaluar el modelo
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f'Mean Squared Error (MSE) de RandomForestRegressor: {mse_rf}')
    """, language = "python")

    st.write("Análisis de Componentes Principales (PCA)")
    st.code("""
# Ajustar PCA
pca_canciones = PCA(n_components = 2)  # Reducir a 2 componentes principales
df_canciones_pca = pca_canciones.fit_transform(df_canciones[numeric_columns_canciones])

# Crear un DataFrame con los componentes principales
df_pca_canciones = pd.DataFrame(df_canciones_pca, columns = ['PCA1', 'PCA2'])

# Visualizar la reducción de dimensionalidad
plt.figure(figsize = (15, 5))
sns.scatterplot(x = 'PCA1', y = 'PCA2', data = df_pca_canciones, s = 100, marker = 'o')
plt.title('Reducción de Dimensionalidad usando PCA', fontsize = 16)
plt.xlabel('PCA1', fontsize = 14)
plt.ylabel('PCA2', fontsize = 14)
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Playlist (df_tracks)")
    st.code("""
# Tamaño de cada cluster en df_tracks
print("Tamaño de cada cluster:")
print(df_tracks['Cluster'].value_counts())
print('') # Espacio en respuesta

# Seleccionar columnas numéricas en df_tracks
numeric_columns_tracks = df_tracks.select_dtypes(include=['number']).columns

# Características promedio por cluster en df_tracks
print("Características promedio por cluster:")
cluster_stats_tracks = df_tracks.groupby('Cluster')[numeric_columns_tracks].mean()
print(cluster_stats_tracks)
print('') # Espacio en respuesta

# Ejemplos representativos por cluster en df_tracks
print("Ejemplos representativos por cluster:")
for cluster_id in df_tracks['Cluster'].unique():
    print(f"Cluster {cluster_id}:")
    print(df_tracks[df_tracks['Cluster'] == cluster_id].head())
    print('') # Espacio en respuesta            
    """, language = "python")

    st.write("Características promedio por cluster en playlists")
    st.code("""
# Graficar las características promedio por cluster
plt.figure(figsize = (15, 5))

# Crear un gráfico de barras para cada característica por cluster
cluster_stats_tracks.plot(kind = 'bar', ax = plt.gca())

plt.title('Características promedio por cluster en playlists', fontsize = 16)
plt.xlabel('Cluster', fontsize = 14)
plt.ylabel('Valor promedio', fontsize = 14)
plt.xticks(rotation = 0)
plt.legend(title = 'Características', bbox_to_anchor = (1.05, 1), loc = 'upper left')
plt.tight_layout()

plt.show()
    """, language = "python")

    st.write("Distribución de clusters en 2D usando PCA")
    st.code("""
# Seleccionar las características numéricas
numeric_columns_tracks = df_tracks.select_dtypes(include = ['number']).columns

# Aplicar PCA para reducir a 2 dimensiones
pca = PCA(n_components = 2)
pca_components = pca.fit_transform(df_tracks[numeric_columns_tracks])

# Crear un DataFrame con las componentes PCA y los clusters
df_pca = pd.DataFrame(data = pca_components, columns = ['PCA1', 'PCA2'])
df_pca['Cluster'] = df_tracks['Cluster']

# Graficar los resultados de PCA
plt.figure(figsize = (15, 5))
sns.scatterplot(x = 'PCA1', y = 'PCA2', hue = 'Cluster', data = df_pca, palette = 'Set1', s = 100, marker = 'o')
plt.title('Distribución de clusters en 2D usando PCA', fontsize = 16)
plt.xlabel('PCA1', fontsize = 14)
plt.ylabel('PCA2', fontsize = 14)
plt.legend(title = 'Cluster')
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Mapa de calor de correlaciones entre características")
    st.code("""
# Calcular la matriz de correlación
correlation_matrix = df_tracks[numeric_columns_tracks].corr()

# Graficar el mapa de calor
plt.figure(figsize = (15, 5))
sns.heatmap(correlation_matrix, annot = True, cmap = 'coolwarm', fmt = '.2f', cbar = True, vmin = -1, vmax = 1)
plt.title('Mapa de calor de correlaciones entre características', fontsize = 16)
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Distribución de Danceability por Cluster")
    st.code("""
# Distribución de características por cluster
plt.figure(figsize=(15, 5))
sns.boxplot(x = 'Cluster', y = 'danceability', data = df_tracks)
plt.title('Distribución de Danceability por Cluster', fontsize = 16)
plt.xlabel('Cluster', fontsize = 14)
plt.ylabel('Danceability', fontsize = 14)
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Centroides de los clusters por característica")
    st.code("""
# Calcular los centroides de cada cluster (ya calculado previamente en cluster_stats_tracks)
centroides = cluster_stats_tracks

# Graficar los centroides de los clusters
centroides.plot(kind = 'bar', figsize = (15, 5), colormap = 'viridis')
plt.title('Centroides de los clusters por característica', fontsize = 16)
plt.xlabel('Características', fontsize = 14)
plt.ylabel('Valor promedio', fontsize = 14)
plt.xticks(rotation = 45)
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Duración promedio por Cluster en las playlists")
    st.code("""
# Duración promedio por cluster
duracion_cluster = df_tracks.groupby('Cluster')['duración (segundos)'].mean()

# Graficar
plt.figure(figsize = (15, 5))
duracion_cluster.plot(kind = 'bar', color = 'lightcoral')
plt.title('Duración promedio por Cluster en las playlists', fontsize = 16)
plt.xlabel('Cluster', fontsize = 14)
plt.ylabel('Duración promedio (segundos)', fontsize = 14)
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Otros modelados para playlist")
    st.write("Reducción de Dimensionalidad con t-SNE")
    st.code("""
# Reducir dimensiones con t-SNE
tsne = TSNE(n_components = 2, random_state = 42)
tsne_components = tsne.fit_transform(df_tracks[numeric_columns_tracks])

# Graficar t-SNE
plt.figure(figsize = (15, 5))
plt.scatter(tsne_components[:, 0], tsne_components[:, 1], c = df_tracks['Cluster'], cmap = 'viridis', s = 100, alpha = 0.7)
plt.title('Distribución de clusters con t-SNE', fontsize = 16)
plt.xlabel('t-SNE 1', fontsize = 14)
plt.ylabel('t-SNE 2', fontsize = 14)
plt.colorbar(label = 'Cluster')
plt.tight_layout()
plt.show()
    """, language = "python")

    st.write("Modelado de Clasificación: Random Forest o XGBoost")
    st.code("""
# Separar variables predictoras y la variable objetivo
X = df_tracks[numeric_columns_tracks]
y = df_tracks['Cluster']

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

# Crear el modelo
rf_model = RandomForestClassifier(n_estimators = 100, random_state = 42)

# Entrenar el modelo
rf_model.fit(X_train, y_train)

# Predecir y evaluar el modelo
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))
    """, language = "python")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### Soy un separador ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

# Algoritmos
with st.expander("Algoritmos"):
    st.write("Herramientas + datos")
    st.code("""
# Herramientas
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Cargar los datos
playlists = pd.read_csv('playlists1.csv')  # Información general de las playlists
canciones = pd.read_csv('canciones_total.csv')  # Características de las canciones
tracks_playlists = pd.read_csv('tracks_playlists.csv')  # Relación entre playlists y canciones
            
# Realizamos la unión usando 'Canción ID' de tracks_playlists y 'canción id' de canciones
tracks_playlists_info = pd.merge(
    tracks_playlists, 
    canciones[['canción id', 'danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']], 
    left_on='Canción ID', 
    right_on='canción id', 
    how='inner'
)

# Verificamos el DataFrame resultante
print(tracks_playlists_info.head())
            
# Agrupar por 'Playlist ID' y calcular el promedio de las características acústicas
playlist_features = tracks_playlists_info.groupby('Playlist ID')[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']].mean().reset_index()

# Unir esta información con el DataFrame de playlists para obtener la información completa
playlist_features = pd.merge(playlists, playlist_features, on='Playlist ID')

# Ahora 'playlist_features' tiene las características promedio de las playlists
    """, language = "python")

    st.write("Ingresar la ID playlist que queramos")
    st.code("""
playlist_usuario_id = "3IyNJEsknaSFoUIn8qf1Lr"
    """, language = "python")

    st.code("""
# Supongamos que el usuario selecciona una playlist (por ejemplo, 'Playlist ID' = 1)

# Obtener las canciones en esa playlist
playlist_usuario_canciones = tracks_playlists_info[tracks_playlists_info['Playlist ID'] == playlist_usuario_id]

# Promediamos las características de las canciones de esa playlist
playlist_usuario_features = playlist_usuario_canciones[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']].mean().values.reshape(1, -1)

# Extraer las características acústicas de todas las canciones
canciones_features = canciones[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']]

# Calcular la similitud entre la playlist del usuario y todas las canciones
similitud_canciones = cosine_similarity(playlist_usuario_features, canciones_features)

# Ordenar las canciones por similitud (de mayor a menor)
indices_similares = similitud_canciones.argsort()[0][::-1]

# Obtener las canciones más similares (por ejemplo, las 5 primeras)
canciones_recomendadas = canciones.iloc[indices_similares[:5]]
print(canciones_recomendadas[['nombre', 'artistas']])
            
# Obtener las características acústicas de la playlist del usuario
playlist_usuario_features = playlist_features[playlist_features['Playlist ID'] == playlist_usuario_id][['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']].values

# Calcular la similitud del coseno entre la playlist del usuario y todas las playlists
similitud_playlists = cosine_similarity(playlist_usuario_features, playlist_features[['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness']])

# Ordenar las playlists por similitud (de mayor a menor)
indices_similares_playlists = similitud_playlists.argsort()[0][::-1]

# Obtener las playlists más similares (por ejemplo, las 5 primeras)
playlists_recomendadas = playlist_features.iloc[indices_similares_playlists[:5]]
print(playlists_recomendadas[['Nombre Playlist', 'Descripción']])
    """, language = "python")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### Soy un separador ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

# Creación de BBDD en MySQL
with st.expander("Código SQL en MySQL para la creación de la base de datos"):
    st.code("""
    CREATE DATABASE Proyecto_Spotify;

    USE Proyecto_Spotify;

    CREATE TABLE artistas (
        artista_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL UNIQUE,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    CREATE TABLE canciones (
        cancion_id VARCHAR(50) PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        artista_id INT,
        duracion_segundos FLOAT NOT NULL,
        popularidad INT DEFAULT 0,
        explicito BOOLEAN DEFAULT FALSE,
        fecha_lanzamiento DATE,
        danceability FLOAT CHECK (danceability BETWEEN 0 AND 1),
        energy FLOAT CHECK (energy BETWEEN 0 AND 1),
        valence FLOAT CHECK (valence BETWEEN 0 AND 1),
        tempo FLOAT,
        acousticness FLOAT CHECK (acousticness BETWEEN 0 AND 1),
        instrumentalness FLOAT CHECK (instrumentalness BETWEEN 0 AND 1),
        speechiness FLOAT CHECK (speechiness BETWEEN 0 AND 1),
        url_spotify VARCHAR(255),
        imagen TEXT,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (artista_id) REFERENCES artistas(artista_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );

    CREATE TABLE playlist (
        cancion_id VARCHAR(50) NOT NULL,
        playlist_id VARCHAR(50),
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (cancion_id, playlist_id),
        FOREIGN KEY (cancion_id) REFERENCES canciones(cancion_id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
    );
    """, language = "sql")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### Soy un separador ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# Importar datos a MySQL con Python / SQLAlchemy
with st.expander("Código Python para conexión y carga de datos"):
    st.code("""
# Herramientas.
import pandas as pd
import sqlalchemy # Para ver la versión
from sqlalchemy import create_engine, text
from datetime import datetime

# Versiones
print(f'pandas: {pd.__version__}')
print(f'sqlalchemy: {sqlalchemy.__version__}')
print('')

# Configurar conexión
user = 'root'
password = 'Jp261191.'
database = 'Proyecto_Spotify'
host = "localhost"
port = 3306

# Crear conexión
engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost/{database}')

# Abrir conección
connection = engine.connect()

# Cargar DF.
df_original = pd.read_csv('playlist_info_con_audio_features.csv')
df = pd.read_csv('datos_canciones.csv')

# Eliminar duplicados para generar el DataFrame de artistas
artistas_df = df[['Artistas']].drop_duplicates().rename(columns = {'Artistas': 'nombre'})

# Reemplazar nulos o vacíos con 'Desconocido'
artistas_df['nombre'] = artistas_df['nombre'].fillna('Desconocido')

# Crear lista de diccionarios con los artistas para insertarlos
artistas_data = artistas_df.to_dict(orient = 'records')

# Insertar con 'INSERT IGNORE' para evitar duplicados
try:
    with engine.connect() as connection:
        
        # Establecer autoincremento a X + 1
        connection.execute(text("ALTER TABLE artistas AUTO_INCREMENT = 1"))

        # Insertar artistas en la base de datos
        for artista in artistas_data:
            query = text("INSERT IGNORE INTO artistas (nombre) VALUES (:nombre)")
            connection.execute(query, artista)  # Usar el diccionario directamente
        
        # Confirmar la transacción
        connection.commit()
    print("Datos de artistas insertados exitosamente.")
except Exception as e:
    print("Error al insertar datos en la tabla 'artistas':", str(e))

# Total de registros en la tabla 'artistas'
with engine.connect() as connection:
    total_artistas = pd.read_sql('SELECT COUNT(*) FROM artistas', connection)
    print(f"Total de artistas en la base de datos: {total_artistas.iloc[0, 0]}")

# Eliminar duplicados y renombrar columnas
canciones_df = df[['Canción ID', 'Nombre', 'Artistas', 'Duración (segundos)', 'Popularidad', 'Explícito', 
                   'Fecha de Lanzamiento', 'Url de Spotify', 'Imagen', 'Danceability', 'Energy', 'Valence', 
                   'Tempo', 'Acousticness', 'Instrumentalness', 'Speechiness']].drop_duplicates()

# Renombrar columnas.
canciones_df = canciones_df.rename(columns={
    'Canción ID': 'cancion_id',
    'Nombre': 'nombre',
    'Artistas': 'artista_nombre',
    'Duración (segundos)': 'duracion_segundos',
    'Popularidad': 'popularidad',
    'Explícito': 'explicito',
    'Fecha de Lanzamiento': 'fecha_lanzamiento',
    'Url de Spotify': 'url_spotify',
    'Imagen': 'imagen',
    'Danceability': 'danceability',
    'Energy': 'energy',
    'Valence': 'valence',
    'Tempo': 'tempo',
    'Acousticness': 'acousticness',
    'Instrumentalness': 'instrumentalness',
    'Speechiness': 'speechiness'
})

# Reemplazar NaNs en columnas críticas
canciones_df['nombre'] = canciones_df['nombre'].fillna('Desconocido')
canciones_df['artista_nombre'] = canciones_df['artista_nombre'].apply(lambda x: None if pd.isna(x) else x)
canciones_df['imagen'] = canciones_df['imagen'].apply(lambda x: None if pd.isna(x) else x)
canciones_df['fecha_lanzamiento'] = pd.to_datetime(canciones_df['fecha_lanzamiento'], errors='coerce')
canciones_df['fecha_lanzamiento'] = canciones_df['fecha_lanzamiento'].fillna('2000-01-01')

# Obtener IDs de los artistas de la base de datos para fusionar
with engine.connect() as connection:
    artistas_db_df = pd.read_sql('SELECT artista_id, nombre FROM artistas', connection)

# Fusionar el DataFrame con los IDs de los artistas
canciones_df = canciones_df.merge(artistas_db_df, left_on='artista_nombre', right_on='nombre', how='left')

# Renombrar 'nombre_x' a 'nombre'
canciones_df['nombre'] = canciones_df['nombre_x']
canciones_df.drop(columns=['nombre_x'], inplace=True, errors='ignore')

# Convertir 'artista_id' a int64 si no hay valores nulos
canciones_df['artista_id'] = canciones_df['artista_id'].astype('Int64', errors='ignore')

# Verificar que 'nombre' esté correctamente definida
if 'nombre' not in canciones_df.columns:
    print("Columna 'nombre' no encontrada. Verificando columnas disponibles.")
    print(canciones_df.columns)

# Cantidad de canciones
total_canciones = len(canciones_df)

# Insertar en base de datos
try:
    with engine.connect() as connection:
        
        # Insertar las canciones en la base de datos usando 'INSERT IGNORE' para evitar duplicados
        query = text('''INSERT IGNORE INTO canciones 
                (cancion_id, nombre, artista_id, duracion_segundos, popularidad, explicito, fecha_lanzamiento, 
                 danceability, energy, valence, tempo, acousticness, instrumentalness, speechiness, 
                 url_spotify, imagen) 
                VALUES 
                (:cancion_id, :nombre, :artista_id, :duracion_segundos, :popularidad, :explicito, :fecha_lanzamiento, 
                 :danceability, :energy, :valence, :tempo, :acousticness, :instrumentalness, :speechiness, 
                 :url_spotify, :imagen)''')
        
        # Insertar todas las canciones de una sola vez
        connection.execute(query, canciones_df.to_dict(orient='records'))
        connection.commit()
        
        print(f"Datos cargados exitosamente en la base de datos. Total de canciones insertadas: {total_canciones}")
except Exception as e:
    print(f"Error al insertar los datos: {str(e)}")

# CSV
df_playlist = pd.read_csv('tracks_playlists.csv')

# Renombrar columnas para que coincidan con los nombres en la base de datos
df_playlist = df_playlist.rename(columns={
    'Canción ID': 'cancion_id',
    'Playlist ID': 'playlist_id'
})

# Eliminar valores nulos en 'cancion_id' o 'playlist_id'
df_playlist = df_playlist.dropna(subset=['cancion_id', 'playlist_id'])

# Eliminar duplicados (en caso de combinaciones repetidas de cancion_id y playlist_id)
df_playlist = df_playlist.drop_duplicates(subset=['cancion_id', 'playlist_id'])

# Validar tamaños antes de la inserción
total_playlists_original = len(df_playlist)
print(f"Total de filas después de limpiar valores nulos y duplicados: {total_playlists_original}")

# Insertar datos en BBDD
try:
    with engine.connect() as connection:
        # Query para insertar datos en playlist
        query = text('''INSERT IGNORE INTO playlist 
                        (cancion_id, playlist_id, updated)
                        VALUES 
                        (:cancion_id, :playlist_id, CURRENT_TIMESTAMP)''')
        
        # Convertir el DataFrame a una lista de diccionarios para la inserción
        data_to_insert = df_playlist.to_dict(orient='records')
        
        # Ejecutar la inserción
        result = connection.execute(query, data_to_insert)
        connection.commit()
        
        # Verificar cuántos registros se insertaron
        rows_inserted = result.rowcount
        print(f"Datos cargados exitosamente en la base de datos. Total de playlists insertadas: {rows_inserted}")
        print(f"Total de playlists procesadas: {total_playlists_original}")
except Exception as e:
    print(f"Error al insertar los datos: {str(e)}")
    """, language = "python")
