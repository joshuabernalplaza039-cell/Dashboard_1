import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURACIÓN DE NIVEL EMPRESARIAL
st.set_page_config(page_title="Data Intelligence System", layout="wide", page_icon="📊")

# 2. ESTILO CSS REFINADO (Barra lateral Midnight & Contenido White-Smoke)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* BARRA LATERAL - DISEÑO INDUSTRIAL */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important; /* Azul Medianoche Profundo */
        border-right: 1px solid #1E293B;
    }
    
    /* Títulos y texto en Sidebar */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    [data-testid="stSidebar"] p {
        color: #94A3B8 !important;
    }

    /* Estilo del Menú de Radio (Navegación) */
    div[data-testid="stSidebarUserContent"] .stRadio label {
        background-color: transparent !important;
        color: #94A3B8 !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin-bottom: 4px !important;
        transition: all 0.2s ease;
        border: none !important;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label:hover {
        background-color: #1E293B !important;
        color: #3B82F6 !important;
    }

    /* Elemento seleccionado del menú */
    div[data-testid="stSidebarUserContent"] .stRadio label[data-selected="true"] {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    /* CARDS DE MÉTRICAS */
    .metric-container {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #E2E8F0;
        text-align: left;
    }
    
    .metric-label {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: #0F172A;
        font-size: 1.8rem;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BAR
