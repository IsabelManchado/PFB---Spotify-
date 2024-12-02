import pandas as pd
import streamlit as st
from Modules.graficos_sprint_2 import atributos
from Modules.enlace_playlist import playlist
from Modules.playlist_usuario import collect_data
from Modules.algoritmos import algoritmo

def app_recomendador():
    
    
    # Título principal
    st.markdown('<h1 class="title">Recomendador</h1>', unsafe_allow_html=True)
    st.write("En esta sección podrás introducir tus playlist favoritas y te mostraremos canciones que creemos te encantarán.")

    # Estilo CSS para el diseño
    st.markdown("""
        <style>
        body {
            background-color: #1A1A44;
            color: white;
            font-family: Arial, sans-serif;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }
        .box {
            background-color: #00FF7F;
            width: 300px;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px;
            border-radius: 8px;
        }
        .title {
            font-size: 40px;
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        .subtitle {
            font-size: 18px;
            margin-top: 20px;
            text-align: center;
            color: #B0B0B0;
        }
        .table-container {
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    

    playlist_url=st.text_input("Ingrese el enlace playlist de una de sus playlists favoritas:")
    playlist_id=playlist(playlist_url)
    if playlist_id:
        playlist_seleccionada = collect_data(playlist_id)
        playlist_seleccionada.columns=["canción id", "nombre", "artistas", "duración (segundos)", "popularidad", "explícito",
                                        "fecha de lanzamiento", "url de spotify", "imagen", "danceability", "energy", "valence", "tempo", "acousticness", "instrumentalness",
                                          "speechiness", "playlist", "clave (key)", "modo (mode)"
]
        
    if playlist_id:
        
        url = playlist_seleccionada["imagen"][0]

        col1, col2, col3, col4, col5 = st.columns([0.5, 1,1,0.5,1], vertical_alignment="center") 
        with col1:
            st.image(url, width=200)
        with col2:
            st.write(playlist_seleccionada["playlist"][0])  
        with col3:
            st.write("")
        with col4:
            st.write("")
        with col5:
            st.write("")
        

            
    else:
        st.warning("Por favor, ingresa un ID de playlist válido.")
    
    
    if playlist_id:

        _, playlists_recomendadas=algoritmo(playlist_id)
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Playlist Seleccionada"):
                df=pd.read_csv(r"..\PFB---Spotify-\EDA\canciones_total.csv")
                df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
                df_playlist_canciones = pd.merge(df_tracks, df, left_on="Canción ID", right_on="canción id")
                playlist_seleccionada_df=df_playlist_canciones[df_playlist_canciones["Playlist ID"]==(playlist_id)]
                playlist_seleccionada_df.columns=['Canción ID', 'Playlist ID',"canción id", "nombre", "artistas", "duración (segundos)", "popularidad", "explícito",
                                        "fecha de lanzamiento", "url de spotify", "imagen", "danceability", "energy", "valence", "tempo", "acousticness", "instrumentalness",
                                          "speechiness", "clave (key)", "modo (mode)","predicted_genre"]
                atributos(playlist_seleccionada_df)
                
        
        with col2:
            with st.expander("Playlists Recomendadas"):
                atributos(playlists_recomendadas)
    
        with st.expander("Conclusiones"):
                columnas=["Playlist ID", "Nombre Playlist", "Descripción","Número de canciones","Url de Spotify"]
                st.write("Playlists recomendadas:",playlists_recomendadas[columnas].reset_index(drop=True))
                st.write("La playlist anterior junto con sus canciones se recomienda debido a la similitud de sus caracteristicas musicales con la playlist elegida")
                data = {"Valence": [playlist_seleccionada_df["valence"].mean(),playlists_recomendadas["valence"].mean()],
                        "Energy": [playlist_seleccionada_df["energy"].mean(),playlists_recomendadas["energy"].mean()],
                        "Danceability": [playlist_seleccionada_df["danceability"].mean(),playlists_recomendadas["danceability"].mean()],
                        "Speechiness":[playlist_seleccionada_df["speechiness"].mean(),playlists_recomendadas["speechiness"].mean()],
                        "Instrumentalness":[playlist_seleccionada_df["instrumentalness"].mean(),playlists_recomendadas["instrumentalness"].mean()],
                        "Accouticness":[playlist_seleccionada_df["acousticness"].mean(),playlists_recomendadas["acousticness"].mean()],
                        "Popularidad":[playlist_seleccionada_df["popularidad"].mean(),playlists_recomendadas["popularidad"].mean()],
                        "Duración":[playlist_seleccionada_df["duración (segundos)"].mean(),playlists_recomendadas["duración (segundos)"].mean()]}
                df = pd.DataFrame(data,index=["Playlist Seleccionada", "Playlist Recomendada"])
                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # Tabla de canciones recomendadas
    st.markdown('<h2 style="text-align: center; margin-top: 30px;">Canciones recomendadas</h2>', unsafe_allow_html=True)

    if playlist_id:
        canciones_recomendadas,_=algoritmo(playlist_id)
        canciones_recomendadas.columns=["Cancion ID", "Nombre", "Artistas", "Duración", "popularidad","explícito","Fecha de Lanzamiento","Url de Spotify","imagen","danceability","energy","valence","tempo","acousticness","instrumentalness","speechiness","clave (key)","modo (mode)","predicted_genre"]
        columnas=["Cancion ID", "Nombre", "Artistas", "Duración", "Fecha de Lanzamiento","Url de Spotify"]

        # Mostrar tabla en un diseño estilizado
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(canciones_recomendadas[columnas], hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    app_recomendador()