import streamlit as st
import pandas as pd
import pymysql

# Datos de los participantes
participants = [
    {
        "name": "Adrián Blanco Ajenjo",
        "linkedin": "https://www.linkedin.com/in/adrianblancoajenjo/",
        "github": "https://github.com/AdriBlanco0",
        "image": "https://media.licdn.com/dms/image/v2/D4D03AQGGRw5wqvRtIw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1712242604340?e=1738195200&v=beta&t=s74NLNdvZemLwPVekmUROTfD7-73U1EK3GInaReoXng"
    },
    {
        "name": "Isabel Manchado Rodríguez",
        "linkedin": "https://www.linkedin.com/in/isabel-manchado-rodríguez-b10363158",
        "github": "https://github.com/IsabelManchado",
        "image": "https://media.licdn.com/dms/image/v2/C4E03AQEwDvPU4TrsgQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1517055886661?e=1738195200&v=beta&t=4eiqMLqtV5t7JfM6L6dgxEMQUiT-aRDAJ0tUiODFWNI"
    },
    {
        "name": "Juan Pablo Riesgo",
        "linkedin": "https://www.linkedin.com/in/riesgo-juan-pablo/",
        "github": "https://github.com/geshnika",
        "image": "https://media.licdn.com/dms/image/v2/D4D03AQFEJUgv_wRE6Q/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1674702020088?e=1738195200&v=beta&t=GeRub95bG9eBUtZYyQju1nlQ9p5zenWTIwJZ8-Tx_Y4"
    },
    {
        "name": "Paola Altea Buonaiuto",
        "linkedin": "https://www.linkedin.com/in/paola-buonaiuto/",
        "github": "https://github.com/binglitch",
        "image": "https://media.licdn.com/dms/image/v2/C4E03AQHX0-gDVgA43w/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1580325250192?e=1738195200&v=beta&t=BBbDNsOIRSz1C5RExpwLEy-FCxBmXzZ09CuCQV6o52o"
    }
]

# Configuración de la página de Streamlit
st.set_page_config(
    page_title = "About Us",
    page_icon = "👥",
    layout = "centered"
)

# Título de la página
st.title("About Us")
st.write("Nos conocimos durante el bootcamp de Hack a Boss en Data Science & AI. A pesar de nuestras diversas edades y nacionalidades, nos une una pasión común por la innovación y la solución de problemas. Estamos convencidos de que la colaboración y el trabajo en equipo son esenciales, y que la diversidad de perspectivas enriquece nuestra creatividad y mejora nuestra capacidad de encontrar soluciones efectivas.")
st.write("Buscamos impactar positivamente a través de la tecnología y la innovación continua")

# Mostrar información de cada participante
for participant in participants:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <h3>{participant['name']}</h3>
            <img src="{participant['image']}" alt="{participant['name']}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 10px;">
            <p>
                <a href="{participant['linkedin']}" target="_blank" style="text-decoration: none; color: #0077b5; font-weight: bold;">LinkedIn</a> |
                <a href="{participant['github']}" target="_blank" style="text-decoration: none; color: #333; font-weight: bold;">GitHub</a>
            </p>
        </div>
        <hr style="margin: 30px 0;">
        """,
        unsafe_allow_html = True
    )
