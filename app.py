# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 18:01:15 2025

@author: jperezr
"""

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

st.title("📍 Ubicaciones de CAP´s de las AFORE y propuesta de nuevos CAP's por cada entidad federativa de la República Mexicana, utilizando el modelo de Huff.")
