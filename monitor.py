import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta

# Configuración de página
st.set_page_config(page_title="Monitor de sitios web", page_icon=":chart_with_upwards_trend:")

# Encabezado de la página
st.markdown("<h1 style='text-align: center;'>Monitor de sitios web</h1>", unsafe_allow_html=True)
st.write(" ")

# URL a monitorear
url = st.text_input("Ingresa la URL del sitio web que deseas monitorear:")

# Verificar que la URL ingresada es válida
if not url.startswith("http"):
    st.warning("Ingresa una URL válida (que empiece con http o https).")
else:
    # Tabla para mostrar el historial de disponibilidad
    uptime_history = pd.DataFrame(columns=["Tiempo", "Disponible"])
    chart_data = pd.DataFrame(columns=["Tiempo", "Disponible"])

    # Parámetros de monitoreo
    delay = 10  # segundos entre cada verificación
    error_counter = 0  # contador de errores consecutivos

    # Monitoreo
    while True:
        try:
            response = requests.get(url)
            status_code = response.status_code
            if status_code == 200:
                st.success("Sitio web disponible.")
                error_counter = 0
            else:
                st.warning(f"El sitio web responde con un código de estado {status_code}.")
                error_counter += 1
        except:
            st.error("Error al acceder al sitio web.")
            error_counter += 1

        # Agregar registro al historial de disponibilidad
        time_now = datetime.now(timezone(-timedelta(hours=4)))
        uptime_history.loc[len(uptime_history)] = [time_now, status_code == 200]

        # Actualizar gráfico de uptime
        chart_data = uptime_history.groupby(pd.Grouper(key="Tiempo", freq="H")).mean()
        chart_data = chart_data.reset_index().rename(columns={"Disponible": "Uptime"})
        chart = (
            alt.Chart(chart_data, height=300)
            .mark_line()
            .encode(
                x="Tiempo:T",
                y=alt.Y("Uptime:Q", axis=alt.Axis(format="0.0%")),
                tooltip=[alt.Tooltip("Tiempo:T", format="%Y-%m-%d %H:%M"), "Uptime"],
            )
            .properties(title="Nivel de uptime")
        )
        st.altair_chart(chart, use_container_width=True)

        # Esperar un tiempo antes de hacer la próxima verificación
        time.sleep(delay)
