import streamlit as st

def menu_stream(context="default"):
    with st.container():
        menu = st.radio(
            "Seleccione una sección",
            [
                "HomePage",
                "Top Tracks",
                "Para creadores",
                "Comparador",
                "Recomendador",
                "Base de datos",
                "Cómo y porqué",
                "About",
            ],
            
            horizontal=True,
            key=f"main_menu_{context}"  # Clave única basada en el contexto
        )

    # Menú lateral
    with st.sidebar:
        st.header("Menú Lateral")
        option = st.radio(
            "Selecciona una opción:", 
            ["Playlist", "Canciones"],
            key=f"sidebar_menu_{context}"  # Clave única basada en el contexto
        )

    return menu, option

