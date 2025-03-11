# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:17:17 2025

@author: jperezr
"""

import pandas as pd
import streamlit as st

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Mostrar el nombre del creador en la barra lateral
st.sidebar.markdown("### Creado por: **Javier Horacio Pérez Ricárdez**")   

st.sidebar.markdown("Marzo del 2025")  


# Sección de Ayuda en la barra lateral
def mostrar_ayuda():
    st.sidebar.title("ℹ️ Ayuda")
    st.sidebar.markdown("""
    ### 📌 Sobre esta aplicación
    Esta aplicación permite visualizar datos filtrados por estado y acceder a enlaces relacionados.

    ### 🛠 ¿Cómo usarla?
    1. **Carga de datos**: Se importan los datos desde un archivo CSV.
    2. **Visualización de datos**: Se muestra el dataset completo.
    3. **Selección de estado**: El usuario elige un estado desde un menú desplegable.
    4. **Filtrado de datos**: Se presentan únicamente los datos del estado seleccionado.
    5. **Acceso a enlaces**: Se muestra un enlace al mapa del estado seleccionado con los CAP's de las AFORE.

    ### ⚠️ Notas
    - Asegúrate de que el archivo `data.csv` contiene las columnas **Estado** y **Enlace**.
    - Si un estado no tiene enlace, aparecerá una advertencia.
    """)

# Mostrar la ayuda en la barra lateral
mostrar_ayuda()

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data.csv')  # Asegúrate de que el CSV contiene la columna "Enlace"
    return df

# Interfaz en Streamlit
st.title('Visualización de Datos por Estado')

# Cargar el dataframe
df = cargar_datos()

# Mostrar el dataframe completo
st.subheader("Datos Completos")
st.dataframe(df)

# Selección de estado
estado_seleccionado = st.selectbox('Selecciona un estado', df['Estado'].unique())

# Filtrar el dataframe según el estado seleccionado
df_filtrado = df[df['Estado'] == estado_seleccionado]

# Mostrar el dataframe filtrado
st.subheader(f"Datos Filtrados para {estado_seleccionado}")
st.dataframe(df_filtrado)

# Obtener el enlace correspondiente al estado seleccionado
enlace_estado = df_filtrado['Enlace'].iloc[0] if not df_filtrado['Enlace'].isna().all() else None

# Mostrar el enlace si está disponible
if enlace_estado:
    st.markdown(f"[Enlace para {estado_seleccionado}]({enlace_estado})", unsafe_allow_html=True)
else:
    st.warning("No hay enlace disponible para este estado.")

