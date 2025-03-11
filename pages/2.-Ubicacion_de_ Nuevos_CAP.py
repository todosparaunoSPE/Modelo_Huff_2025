# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:57:36 2025

@author: jperezr
"""

import pandas as pd
import numpy as np
import streamlit as st
from geopy.distance import geodesic


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

# Cargar los datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data1.csv')  # Asegúrate de que el CSV contiene la columna "Enlace"

    # Limpiar la columna 'PEA' (eliminar comas y convertir a número)
    df['PEA'] = df['PEA'].replace({',': ''}, regex=True).astype(float)
    
    # Asegurarse de que latitud y longitud son numéricas
    df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
    df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')

    # Filtrar filas con valores nulos en latitud, longitud, PEA y Enlace
    df = df.dropna(subset=['latitud', 'longitud', 'PEA', 'Enlace'])

    return df

# Función para calcular la distancia entre dos puntos usando la fórmula Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# Función para calcular la ubicación de un nuevo CAP usando el modelo de Huff
def calcular_ubicacion_nuevo_cap(df, estado_seleccionado, b=2.0):
    # Filtrar los datos por el estado seleccionado
    cap_estado = df[df['Estado'] == estado_seleccionado]
    
    # Coordenadas del nuevo CAP (por ejemplo, el centro geográfico del estado)
    lat_nuevo_cap = cap_estado['latitud'].mean()
    lon_nuevo_cap = cap_estado['longitud'].mean()

    # Calcular la distancia de cada CAP al nuevo CAP
    cap_estado['distancia'] = cap_estado.apply(
        lambda row: calcular_distancia(lat_nuevo_cap, lon_nuevo_cap, row['latitud'], row['longitud']),
        axis=1
    )
    
    # Calcular la probabilidad de elección de cada CAP usando el modelo de Huff
    cap_estado['probabilidad'] = cap_estado['atracción'] / (cap_estado['distancia'] ** b)
    
    # Normalizar las probabilidades
    probabilidad_total = cap_estado['probabilidad'].sum()
    cap_estado['probabilidad_normalizada'] = cap_estado['probabilidad'] / probabilidad_total
    
    # Elegir un nuevo CAP basado en las probabilidades
    nuevo_cap = cap_estado.sample(weights=cap_estado['probabilidad_normalizada'], n=1)
    
    # Devolver el estado y la ubicación del nuevo CAP
    lat_nuevo_cap = nuevo_cap['latitud'].values[0]
    lon_nuevo_cap = nuevo_cap['longitud'].values[0]
    
    return pd.DataFrame({
        'Estado': [estado_seleccionado],
        'Latitud del Nuevo CAP': [lat_nuevo_cap],
        'Longitud del Nuevo CAP': [lon_nuevo_cap]
    })

# Interfaz de Streamlit
st.title('Simulación de Ubicación de Nuevo CAP usando el Modelo de Huff')

# Cargar datos de los CAPs y los estados
df = cargar_datos()

# Selección de estado
estado_seleccionado = st.selectbox('Selecciona un estado', df['Estado'].unique())

# Calcular la ubicación del nuevo CAP usando el modelo de Huff
df_nuevo_cap = calcular_ubicacion_nuevo_cap(df, estado_seleccionado)

# Mostrar los resultados
st.write(f"Ubicación del nuevo CAP en el estado de {estado_seleccionado}:")
st.write(df_nuevo_cap)

# Obtener y mostrar el enlace correspondiente al estado seleccionado
enlace_estado = df[df['Estado'] == estado_seleccionado]['Enlace'].iloc[0] if not df[df['Estado'] == estado_seleccionado]['Enlace'].isna().all() else None

if enlace_estado:
    st.markdown(f"[Ver más información sobre {estado_seleccionado}]({enlace_estado})", unsafe_allow_html=True)
else:
    st.warning("No hay enlace disponible para este estado.")
    
    
    



# Mostrar el nombre del creador en la barra lateral
st.sidebar.markdown("### Creado por: **Javier Horacio Pérez Ricárdez**")    
    
st.sidebar.markdown("Marzo del 2025") 


# Sección de Ayuda
def mostrar_ayuda():
    st.sidebar.title("Ayuda")
    st.sidebar.markdown("""
    ### 📌 Sobre esta aplicación
    Esta aplicación utiliza el **Modelo de Huff** para determinar la mejor ubicación para un nuevo Centro de Atención Pública (CAP).
    
    ### 🛠 ¿Cómo funciona?
    1. **Carga de datos**: Se importan los datos de los CAP existentes, incluyendo su ubicación geográfica y el número de personas económicamente activas (*PEA*).
    2. **Selección de Estado**: El usuario elige un estado para realizar el análisis.
    3. **Cálculo de distancias**: Se calcula la distancia entre los CAP existentes y el posible nuevo CAP.
    4. **Modelo de Huff**: Se determina la probabilidad de elección de un nuevo CAP basado en la atracción del mercado y la distancia.
    5. **Ubicación óptima**: Se selecciona la mejor ubicación basándose en probabilidades normalizadas.

    ### ℹ️ Notas
    - La atracción de cada CAP es un parámetro clave para el cálculo.
    - La fórmula de Huff toma en cuenta la relación inversa entre distancia y elección.
    - Se usa **geopy** para calcular distancias entre coordenadas geográficas.
    """)

# Mostrar la ayuda en la barra lateral
mostrar_ayuda()    
    
    
    
    
    
    
    
