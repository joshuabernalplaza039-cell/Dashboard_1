import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. SETUP DE PÁGINA
st.set_page_config(page_title="Intelligence Hub", layout="wide", page_icon="⚙️")

# 2. CSS PARA BARRA LATERAL DINÁMICA
st.markdown("""
    <style>
    /* Estética de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
        min-width: 300px !important;
    }
    
    /* Efecto de cristal en los selectores */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1E293B !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 8px;
    }

    /* Títulos de sección en Sidebar */
    .sidebar-section-title {
        color: #64748B;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 20px 0px 10px 0px;
    }

    /* Tarjetas de estado en la parte inferior de la barra lateral */
    .status-card {
        background: #1E293B;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL DINÁMICA
with st.sidebar:
    st.markdown("<h2 style='color: white;'>ANALYTICS <span style='color: #3B82F6;'>V5</span></h2>", unsafe_allow_html=True)
    
    # --- SECCIÓN 1: NAVEGACIÓN PRINCIPAL ---
    st.markdown('<p class="sidebar-section-title">Módulos del Sistema</p>', unsafe_allow_html=True)
    menu_principal = st.selectbox(
        "Seleccionar Módulo",
        ["📈 Dashboard General", "🔍 Auditoría Profunda", "🧪 Simulación & Proyección", "📑 Generador de Reportes"],
        label_visibility="collapsed"
    )

    st.divider()

    # --- SECCIÓN 2: CONTROL DINÁMICO (Cambia según el archivo) ---
    st.markdown('<p class="sidebar-section-title">Filtros de Datos</p>', unsafe_allow_html=True)
    archivo = st.file_uploader("Cargar Datos Institucionales", type=["csv", "xlsx"])

    if archivo:
        df = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
        
        # Filtros inteligentes que solo aparecen si hay datos
        columnas_cat = df.select_dtypes(include=['object']).columns.tolist()
        if columnas_cat:
            cat_filter = st.multiselect("Filtrar por Categoría", options=df[columnas_cat[0]].unique())
            if cat_filter:
                df = df[df[columnas_cat[0]].isin(cat_filter)]

        # Selector de Rango de Valores
        columnas_num = df.select_dtypes(include=[np.number]).columns.tolist()
        if columnas_num:
            min_val, max_val = float(df[columnas_num[0]].min()), float(df[columnas_num[0]].max())
            rango = st.slider("Rango de Análisis", min_val, max_val, (min_val, max_val))
            df = df[(df[columnas_num[0]] >= rango[0]) & (df[columnas_num[0]] <= rango[1])]

    # --- SECCIÓN 3: ESTADO DEL SISTEMA ---
    st.markdown('<p class="sidebar-section-title">Estado de Conexión</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="status-card">
            <div style="color: #10B981; font-size: 12px;">● Sistema Activo</div>
            <div style="color: white; font-size: 14px; margin-top:5px;">Base: {"Cargada" if archivo else "Esperando..."}</div>
            <div style="color: #64748B; font-size: 11px;">Latencia: 14ms</div>
        </div>
    """, unsafe_allow_html=True)

# 4. CONTENIDO PRINCIPAL DINÁMICO
if archivo:
    if menu_principal == "📈 Dashboard General":
        st.title("Monitoreo en Tiempo Real")
        
        # Grid de métricas pro
        c1, c2, c3 = st.columns(3)
        c1.metric("Volumen de Datos", f"{len(df):,}", "+12%")
        c2.metric("Calidad de Registro", "98.2%", "0.5%")
        c3.metric("Tiempo de Procesamiento", "0.4s", "-0.1s")

        # Gráfico dinámico
        if len(columnas_num) > 0:
            fig = px.line
