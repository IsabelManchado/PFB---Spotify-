
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from Modules.EDA import collect_data
from Modules.graficos_playlist import graficos
from Modules.Clustering import clustering_canciones,clustering_playlist
from Modules.graficos_sprint_3 import grafico_genero,grafico_artistas1,atributos,graficos_extras,comparador_genero,comparador_artistas,comparador_atributos
from Modules.enplace_playlist import playlist,playlist2
import pymysql


def eda_app():


    st.set_page_config(
    page_title="Spotify Recommender App",      
    page_icon="🎶",                  
    layout="wide",                 
    initial_sidebar_state="collapsed")
    
    alt.themes.enable("dark")

    with st.container():
        colu1, colu2, colu3 = st.columns([2, 6, 2]) 
        with colu1:
            st.image("Modules/logo.PNG", width=900,use_column_width="always")
            
        with colu2:
            with st.container():
                st.subheader("")
            with st.container():
                subcol1, subcol2, subcol3 = st.columns([1, 6, 1])
                with subcol2:
                    menu = st.radio("Seleccione una sección", ["Inicio", "Vista General", "Vistas Específicas", "Conclusiones y Métricas", "About"],index=None, horizontal=True)
     

    if menu == "Inicio":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Spotify Recommender App")
            st.write("Aplicación que le permite navegar y visualizar de manera cómoda y sencilla información y estadísticas de playlist de spotify")
            st.write("Acuda a la seccion Vista General para ingresar el ID de la playlist que le interese analizar, luego navegue a traves de las distintas secciones para obtener toda la información")

        

    elif menu == "Vista General":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Vista General")

            # Entrada para ID de la playlist y base de datos
            #playlist_id = st.text_input("Ingresa el ID de la playlist de Spotify:")
        
            #if st.button("Ejecutar"):
                # if playlist_id:
                #     raw_data = collect_data(playlist_id)
                #     #loaded_data = load_data(raw_data)
                #     url = raw_data["Imagenes"][0]

                #     col1, col2 = st.columns([1, 2], vertical_alignment="center") 
                #     with col1:
                #         st.image(url, use_column_width=True)
                #     with col2:
                #         st.write(raw_data["Playlist"][0])

                #     st.dataframe(raw_data, width=1000,height=350)
                    # st.sidebar.header("Filtros")
                    # artistas_seleccionados = st.sidebar.multiselect("Artista:", options=raw_data["Artistas"].unique(), default=raw_data["Artistas"].unique())
                    # df_filtered = raw_data[raw_data["Artistas"].isin(artistas_seleccionados)]
                    # st.dataframe(df_filtered)
                        
                # else:
                #     st.warning("Por favor, ingresa un ID de playlist válido.")
    
        
            sub_menu = st.sidebar.radio("Subsecciones",["Selecciona una opción","Características Medibles de Canciones",
                "Resumen de Estadísticas de Playlist",
                "Comparador de Canciones",
                "Segmentación de Playlist"])

            if sub_menu == "Selecciona una opción":
                st.write("Por favor, selecciona una opción del menú lateral.")
                

            elif sub_menu == "Características Medibles de Canciones":
                col=st.columns((1,5.5,1))
                with col[1]:
                    st.subheader("Características Medibles de Canciones")
                    st.subheader("")
                    playlist_url=st.text_input("Ingrese el enlace playlist de Spotify:")
                    
                 
                
                col = st.columns((1,1), gap='small')
                with col[0]:
                    st.subheader('Artistas')
                    df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
                    playlist_id=playlist(playlist_url)                   
                    if playlist_id:
                        grafico_artistas1(df, playlist_id)
                        st.markdown("Artistas más escuchados por número total de canciones")
                    
                    

                with col[1]:
                    st.subheader('Géneros')
                    df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
                    playlist_id=playlist(playlist_url)                   
                    if playlist_id:
                        grafico_genero(df,playlist_id)
                    
                    
                    st.markdown("Géneros más escuchados")
                                         
                    
                with st.container():
                    st.subheader('Gráficos Extras')
                    df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
                    playlist_id=playlist(playlist_url)                   
                    if playlist_id:
                        graficos_extras(df,playlist_id)

                       

            elif sub_menu == "Resumen de Estadísticas de Playlist":
                col=st.columns((1.5,5,1))
                with col[1]:
                    st.subheader("Resumen de Estadísticas de Playlist")
                    playlist_url=st.text_input("Ingrese el enlace playlist de Spotify:")
                
                df = pd.read_csv(r'..\PFB---Spotify-\EDA\canciones_total.csv')
                playlist_id=playlist(playlist_url)                   
                if playlist_id:
                    atributos(df,playlist_id)
                    
                
                

                # if playlist_id:
                #     raw_data = collect_data(playlist_id)
            
                #     st.write(f"Mostrando {len(raw_data)} canciones de {len(raw_data)}")
                #     st.write(f"La duración total de las canciones es de {raw_data["Duración (segundos)"].sum()/3600} horas")
                #     st.write("Promedio de las características:")
                #     promedio_caracteristicas=raw_data[["Popularidad","Danceability", "Energy", "Valence", "Tempo", "Acousticness", "Instrumentalness", "Speechiness"]].mean()
                #     for caracteristica, valor in promedio_caracteristicas.items():
                #         st.write(f"**{caracteristica.capitalize()}**: {valor:.2f}")
                
                
                        

            elif sub_menu == "Comparador de Canciones":
                col=st.columns((1,5.5,1))
                with col[1]:
                    st.subheader("Comparador de Canciones")
                    st.subheader("")

                    # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
                    # playlist_options = df_tracks["Playlist ID"].unique()
                    # playlist_id1 = st.selectbox("Selecciona el ID de la primera playlist:", playlist_options)
                    # playlist_id2 = st.selectbox("Selecciona el ID de la segunda playlist:", playlist_options)
                    playlist_url1=st.text_input("Ingrese los enlaces de las playlists:")
                    playlist_url2=st.text_input("")
                playlist_ids = playlist2(playlist_url1, playlist_url2)
                if len(playlist_ids) == 2:
                    playlist_id1 = playlist_ids[0]
                    playlist_id2 = playlist_ids[1]

                    col = st.columns((1,1), gap='small')
                    with col[0]:
                        st.subheader('Artistas')
                        
                        if playlist_id1 and playlist_id2:
                            comparador_artistas(playlist_id1,playlist_id2)
                        
                        st.markdown("Comparación de Artistas por Playlist")
                        

                    with col[1]:
                        if playlist_id1 and playlist_id2:
                            comparador_genero(playlist_id1,playlist_id2)
                        
                        st.markdown("Comparación de géneros por Playlist")
                    
                    with st.container():
                        st.subheader('Media de atributos')
                        if playlist_id1 and playlist_id2:
                            comparador_atributos(playlist_id1,playlist_id2)
                        
                        st.markdown("Comparación de atributos por Playlist")
                else:
                        st.error("No se pudieron extraer ambas playlists. Verifique los enlaces ingresados.")

            
            elif sub_menu == "Segmentación de Playlist":
                col=st.columns((2,4,1))
                with col[1]:
                    st.subheader("Segmentación de Playlist")
                    st.subheader("")
                playlist_url=st.text_input("Ingrese el enlace playlist de Spotify:")
                playlist_id=playlist(playlist_url)
                st.subheader('Gráficos dispersión canciones de la playlist seleccionada')
                # df_tracks = pd.read_csv(r"..\PFB---Spotify-\EDA\Tracks_playlists.csv")
                # playlist_options = df_tracks["Playlist ID"].unique()
                # playlist_id = st.selectbox("Selecciona el ID de la playlist de Spotify:", playlist_options)
                # if st.button("Ok"):
                #     if playlist_id:
                               
                if playlist_id:
                    clustering_canciones(playlist_id)
                st.markdown("Este gráfico muestra la distribución de los clusteres reduciendo a dos dimensiones las características por el método PCA")
                            
                st.subheader("")
                st.subheader('Gráficos dispersión de todas las playlists de la base de datos')
                if playlist_id:
                    clustering_playlist() 
                st.markdown("Este gráfico muestra la distribución de los clusteres reduciendo a dos dimensiones las características por el método PCA")
    
    elif menu == "Vistas Específicas":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Vistas Específicas")
        
            playlist_url=st.text_input("Ingrese el enlace playlist de Spotify:")
            playlist_id=playlist(playlist_url)
        
            if st.button("Ejecutar"):
                if playlist_id:
                    raw_data = collect_data(playlist_id)
                    url = raw_data["Imagenes"][0]
                    col1, col2 = st.columns([1, 2], vertical_alignment="center") 
                    with col1:
                        st.image(url, use_column_width=True)
                    with col2:
                        st.write(raw_data["Playlist"][0])
            sub_menu = st.sidebar.radio("Seleccione una vista", [
            "Vista Detallada de Segmentación",
            "Recomendador de Canciones"
        ])

            if sub_menu == "Vista Detallada de Segmentación":
                st.write("***COMPLETAR ***")

            elif sub_menu == "Recomendador de Canciones":
                st.subheader("Recomendador de Canciones")
                st.write("***COMPLETAR***")

            
    elif menu == "Conclusiones y Métricas":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Conclusiones y Métricas")
            playlist_id = st.text_input("Ingresa el ID de la playlist de Spotify:")
        
            if st.button("Ejecutar"):
                
                if playlist_id:
                    raw_data = collect_data(playlist_id)
                    url = raw_data["Imagenes"][0]
                    col1, col2 = st.columns([1, 2], vertical_alignment="center") 
                    with col1:
                        st.image(url, use_column_width=True)
                    with col2:
                        st.write(raw_data["Playlist"][0])
            
            st.write("***COMPLETAR ***")
        # METER CODIGO

    elif menu == "About":
        st.header("About")
        st.write("***COMPLETAR DESCRIPCION***")
    
    st.sidebar.info("Aplicación desarrollada con Streamlit")
        

if __name__ == "__main__":
    eda_app()
