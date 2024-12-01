
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from Modules.Clustering import clustering_canciones,clustering_playlist
from Modules.graficos_sprint_3 import grafico_genero,grafico_artistas,atributos,graficos_extras,comparador_genero,comparador_artistas,comparador_atributos,comparador_genero_canciones1,comparador_artistas_canciones1,comparador_atributos_canciones1
from Modules.enlace_playlist import playlist,playlist2
from Modules.playlist_usuario import collect_data,predecir_genero_canciones,clustering_canciones1
from Modules.graficos_sprint_3_pl_usuario import grafico_genero1,grafico_artistas1,atributos1,graficos_extras1,comparador_genero1,comparador_artistas1,comparador_atributos1,comparador_genero_cancion,comparador_artistas_canciones,comparador_atributos_canciones
from Modules.Clustering_pl_usuario import clustering_canciones1


def app_comparador():
    # Configurador de la página
    st.set_page_config(
        page_title = "Comparador",
        page_icon = "🔍",
        layout = "wide"
    )
    # Título de la página
    st.markdown('<h1 class="title">Comparador</h1>', unsafe_allow_html=True)
    st.write("En esta sección podrás comparar playlist y canciones desde los artistas y géneros más populares hasta sus características medibles.")
    df_canciones= pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
    df_playlist= pd.read_csv(r'..\PFB---Spotify-\EDA\playlists1.csv') 
    df_tracks= pd.read_csv(r'..\PFB---Spotify-\EDA\Tracks_playlists.csv')
    df_tracks.columns=["canción id","Playlist ID"]
    df_canciones_playlist=pd.merge(df_tracks, df_playlist, on="Playlist ID", how="left")
    df_resultado = pd.merge(df_canciones, df_canciones_playlist, on="canción id", how="left")
    playlist_url1=st.text_input("Ingrese el enlace de una playlist de Spotify:") 
    
    playlist_url2=st.text_input("Ingrese el enlace de la segunda playlist de Spotify:")
    
    playlist_ids = playlist2(playlist_url1, playlist_url2)
    
    playlist_seleccionada1 = collect_data(playlist_ids[0])
    playlist_seleccionada2 = collect_data(playlist_ids[1])
    if len(playlist_ids)==2:
                
                col1, col2, col3, col4, col5 = st.columns((0.5,1,1,0.5,1), gap='small')

                # Columna 1: Imagen de la primera playlist
                with col1:
                    st.image(playlist_seleccionada1["Imagen"][0], width=200)

                # Columna 2: Contenedor para texto pegado a la imagen de col1
                with col2:
                    st.header("")
                    with st.container():
                        st.markdown(
                            f"""
                            <p style="font-size: 18px; align-items: start; text-align: start; margin: 0;">
                                {playlist_seleccionada1["Playlist"][0]}
                            </p>
                            """,
                            unsafe_allow_html=True,
                        )

                # Columna 3: Texto "Vs" centrado
                with col3:
                    st.header("")
                    st.markdown(
                        """
                        <div style="display: flex; align-items: start; justify-content: start; height: 100%; font-size: 24px; font-weight: bold;"> Vs
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Columna 4: Imagen de la segunda playlist
                with col4:
                    st.image(playlist_seleccionada2["Imagen"][0], width=200)

                # Columna 5: Contenedor para texto pegado a la imagen de col4
                with col5:
                    st.header("")
                    with st.container():
                        st.markdown(
                            f"""
                            <p style="font-size: 18px; text-align: start; margin: 0;">
                                {playlist_seleccionada2["Playlist"][0]}
                            </p>
                            """,
                            unsafe_allow_html=True,
                        )


        
                
    
    sub_menu = st.sidebar.radio("Subsecciones",["Selecciona una opción","Playlist",
                "Canciones"])
    if sub_menu == "Selecciona una opción":
                st.write("Por favor, selecciona una opción del menú lateral.")
                

    elif sub_menu == "Playlist":
        playlist_ids = playlist2(playlist_url1, playlist_url2)
        if len(playlist_ids) == 2:
            playlist_id1 = playlist_ids[0]
            playlist_id2 = playlist_ids[1]

            col = st.columns((1,1), gap='small')
            with col[0]:
                with st.expander('Artistas'):
                
                    if playlist_id1 and playlist_id2:
                        comparador_artistas(playlist_id1,playlist_id2)
                    
                    # st.markdown("Comparación de Artistas por Playlist")
                

            with col[1]:
                with st.expander('Géneros'):
                    if playlist_id1 and playlist_id2:
                        comparador_genero(playlist_id1,playlist_id2)
                    
                    # st.markdown("Comparación de géneros por Playlist")
            
            with st.container():
                with st.expander('Media de atributos'):
                    if playlist_id1 and playlist_id2:
                        comparador_atributos(playlist_id1,playlist_id2)
                    
                    #st.markdown("Comparación de atributos por Playlist")
        else:
                st.error("No se pudieron extraer ambas playlists. Verifique los enlaces ingresados.")
    
    elif sub_menu == "Canciones":
         if len(playlist_ids) == 2:
                  

            selected_song1 = st.selectbox("Selecciona la canción que desees de la primera playlist:",playlist_seleccionada1["Nombre"].tolist())

            selected_song2 = st.selectbox("Selecciona la canción que desees de la segunda playlist:", playlist_seleccionada2["Nombre"].tolist())
            
            
            if selected_song1 and selected_song2:
                playlist_ids = playlist2(playlist_url1, playlist_url2)
                    
                playlist_id1 = playlist_ids[0]
                playlist_id2 = playlist_ids[1]
                col = st.columns((1,1), gap='small')
                with col[0]:
                    with st.expander('Artistas'):
                    
                        if selected_song1 and selected_song2:
                            
                            comparador_artistas_canciones1(playlist_id1,playlist_id2,selected_song1,selected_song2)
                        
                        # st.markdown("Comparación de Artistas por Playlist")
                    

                with col[1]:
                    with st.expander("Géneros"):
                        if selected_song1 and selected_song2:
                            comparador_genero_canciones1(playlist_id1,playlist_id2,selected_song1,selected_song2)
                    
                    # st.markdown("Comparación de géneros por Playlist")
                
                with st.container():
                    with st.expander('Media de atributos'):
                        if selected_song1 and selected_song2:
                            comparador_atributos_canciones1(playlist_id1,playlist_id2,selected_song1,selected_song2)
                        
                        # st.markdown("Comparación de atributos por Playlist")
          
         
    

if __name__ == "__main__":
    app_comparador()
