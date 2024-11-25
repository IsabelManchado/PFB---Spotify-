import pandas as pd
import streamlit as st

def playlist(playlist_url):
    playlist_id = None 
    
    if "playlist/" in playlist_url:
        try:
            playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
            st.write(f"ID de la playlist extraído: {playlist_id}")
            
        except IndexError:
            st.error("El enlace ingresado no tiene el formato correcto.")
    elif playlist_url:
            st.warning("Por favor, ingrese un enlace válido de una playlist de Spotify.")
    return playlist_id


def playlist2(playlist_url1,playlist_url2):
    playlist_id1 = None 
    playlist_id2 = None 
    playlist_list=[]
    list=[]
    
    if "playlist/" in playlist_url1 and playlist_url2:
        try:
            playlist_id1 = playlist_url1.split("playlist/")[1].split("?")[0]
            playlist_id2 = playlist_url2.split("playlist/")[1].split("?")[0]
            st.write(f"IDs de las playlists extraídos: {playlist_id1} y {playlist_id2}")
            playlist_list.append(playlist_id1)
            playlist_list.append(playlist_id2)
            
        except IndexError:
            st.error("El enlace ingresado no tiene el formato correcto.")
    elif playlist_url1 and playlist_url2:
            st.warning("Por favor, ingrese un enlace válido de una playlist de Spotify.")
    return playlist_list
        