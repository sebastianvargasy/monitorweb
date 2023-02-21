import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Monitoreo de www.sochisi.cl", page_icon="📈", layout="wide")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>Monitoreo de www.sochisi.cl</h1>", unsafe_allow_html=True)

# Tabla para mostrar los resultados
st.write(" ")
st.write("### Estado del sitio")
table = st.table([])

# Monitoreo del sitio web
while True:
    # Hacemos la petición al sitio web
    url = "http://www.sochisi.cl"
    response = requests.get(url)

    # Obtenemos el estado del sitio web
    if response.status_code == 200:
        status = "En línea"
    else:
        status = "Fuera de línea"

    # Obtenemos la fecha y hora actual
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Agregamos los resultados a la tabla
    data = [[status, now]]
    table.add_rows(data)

    # Esperamos 5 segundos antes de hacer la siguiente petición
    time.sleep(5)
