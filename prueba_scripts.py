
import streamlit as st
from Modules.EDA import collect_data
from Modules.BBDD import creacion_database, load_data
from Modules.graficos_playlist import graficos
import pymysql


def eda_app():


    st.set_page_config(
    page_title="Spotify Recommender App",      
    page_icon="🎶",                  
    layout="centered",                 
    initial_sidebar_state="expanded")
    
    with st.container(border=True):
        menu = st.radio("Seleccione una sección", ["Inicio", "Vista General", "Vistas Específicas", "Conclusiones y Métricas", "About"],index=None, horizontal=True)
     

    if menu == "Inicio":
        st.header("Spotify Recommender App")
        st.write("Aplicación que le permite navegar y visualizar de manera cómoda y sencilla información y estadísticas de playlist de spotify")
        st.write("Acuda a la seccion Vista General para ingresar el ID de la playlist que le interese analizar, luego navegue a traves de las distintas secciones para obtener toda la información")

        

    elif menu == "Vista General":
        st.header("Vista General")

        # Entrada para ID de la playlist y base de datos
        playlist_id = st.text_input("Ingresa el ID de la playlist de Spotify:")
       
        if st.button("Ejecutar"):
            if playlist_id:
                raw_data = collect_data(playlist_id)
                loaded_data = load_data(raw_data)
                url = raw_data["Imagenes"][0]

                col1, col2 = st.columns([1, 2], vertical_alignment="center") 
                with col1:
                    st.image(url, use_column_width=True)
                with col2:
                    st.write(raw_data["Playlist"][0])

                st.dataframe(raw_data, width=1000,height=350)
                # st.sidebar.header("Filtros")
                # artistas_seleccionados = st.sidebar.multiselect("Artista:", options=raw_data["Artistas"].unique(), default=raw_data["Artistas"].unique())
                # df_filtered = raw_data[raw_data["Artistas"].isin(artistas_seleccionados)]
                # st.dataframe(df_filtered)
                    
            else:
                st.warning("Por favor, ingresa un ID de playlist válido.")
    
        
        sub_menu = st.sidebar.radio("Subsecciones",["Selecciona una opción","Características Medibles de Canciones",
            "Resumen de Estadísticas de Playlist",
            "Comparador de Canciones",
            "Segmentación de Playlist"])

        if sub_menu == "Selecciona una opción":
            st.write("Por favor, selecciona una opción del menú lateral.")

        elif sub_menu == "Características Medibles de Canciones":
            if playlist_id:
                raw_data = collect_data(playlist_id)
                
                st.subheader("Características Medibles de Canciones")
                
                heatmap, bubble, scatter, hist, box_plot, violin, area= graficos(raw_data) 
            
                st.plotly_chart(heatmap)
    
                st.plotly_chart(bubble)

                st.plotly_chart(scatter)

                st.plotly_chart(hist)

                st.plotly_chart(box_plot)

                st.plotly_chart(violin)

                st.plotly_chart(area)


        elif sub_menu == "Resumen de Estadísticas de Playlist":
            st.subheader("Resumen de Estadísticas de Playlist")
            if playlist_id:
                raw_data = collect_data(playlist_id)
        
                st.write(f"Mostrando {len(raw_data)} canciones de {len(raw_data)}")
                st.write(f"La duración total de las canciones es de {raw_data["Duración (segundos)"].sum()/3600} horas")
                st.write("Promedio de las características:")
                promedio_caracteristicas=raw_data[["Popularidad","Danceability", "Energy", "Valence", "Tempo", "Acousticness", "Instrumentalness", "Speechiness"]].mean()
                for caracteristica, valor in promedio_caracteristicas.items():
                    st.write(f"**{caracteristica.capitalize()}**: {valor:.2f}")
            
                    

        elif sub_menu == "Comparador de Canciones":
            st.write(f"Mostrando {len(raw_data)} canciones de {len(raw_data)}")
        
        elif sub_menu == "Segmentación de Playlist":
            st.subheader("Segmentación de Playlist")
            # METER CODIGO 
    
    elif menu == "Vistas Específicas":
        st.header("Vistas Específicas")
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
        st.header("Conclusiones y Métricas del Modelo")
        st.write("***COMPLETAR ***")
        # METER CODIGO

    elif menu == "About":
        st.header("About")
        st.write("***COMPLETAR DESCRIPCION***")
    
    st.sidebar.info("Aplicación desarrollada con Streamlit")
        

if __name__ == "__main__":
    eda_app()
