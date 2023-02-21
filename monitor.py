import time
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

# Configuración de página
st.set_page_config(page_title="Monitor Web", page_icon="🕸️", layout="wide")

# Configuración de hora local
local_tz = pytz.timezone('America/Santiago')

# URL del sitio web a monitorear
url = "https://www.sochisi.cl"

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>Monitor Web</h1>", unsafe_allow_html=True)
st.write(" ")
st.write(f"Monitoreando el sitio web {url} cada 60 segundos...")

# Configuración de tabla
col1, col2 = st.columns(2)
with col1:
    st.write("Hora")
with col2:
    st.write("Estado")

# Monitoreo del sitio web
while True:
    try:
        # Realizamos la petición GET al sitio web
        response = requests.get(url)
        response.raise_for_status()

        # Analizamos el contenido HTML de la respuesta
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtenemos la hora actual en Santiago de Chile
        current_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')

        # Agregamos la fila a la tabla
        with col1:
            st.write(current_time)
        with col2:
            st.write("🟢 En línea")

    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        # Obtenemos la hora actual en Santiago de Chile
        current_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')

        # Agregamos la fila a la tabla
        with col1:
            st.write(current_time)
        with col2:
            st.write("🔴 Fuera de línea")

    # Esperamos 60 segundos antes de realizar la siguiente petición
    time.sleep(60)

