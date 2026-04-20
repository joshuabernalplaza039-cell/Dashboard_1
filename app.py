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

# 3. BARRA LATERAL (Navegación Limpia)
with st.sidebar:
    st.markdown("""
        <div style='padding: 20px 0px 40px 0px;'>
            <h2 style='margin:0;'>CORE <span style='color: #3B82F6;'>ANALYTICS</span></h2>
            <p style='margin:0; font-size: 11px; letter-spacing: 1px;'>DATA MANAGEMENT SYSTEM</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "NAV",
        ["Panel Ejecutivo", "Auditoría de Datos", "Reportes Operativos"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📥 Importación")
    archivo = st.file_uploader("Cargar dataset", type=["csv", "xlsx"], label_visibility="collapsed")

# 4. LÓGICA DE CONTENIDO
if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)

    if menu == "Panel Ejecutivo":
        st.title("Monitoreo Estratégico")
        st.markdown("Análisis en tiempo real de indicadores operativos.")
        
        # Fila de métricas personalizadas
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f'<div class="metric-container"><div class="metric-label">Registros</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
        with c2:
            nulos = df.isnull().sum().sum()
            st.markdown(f'<div class="metric-container"><div class="metric-label">Integridad</div><div class="metric-value">{100 - (nulos/df.size*100):.1f}%</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-container"><div class="metric-label">Variables</div><div class="metric-value">{df.shape[1]}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-container"><div class="metric-label">Eficiencia</div><div class="metric-value">94.2%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráficos Pro
        g1, g2 = st.columns([2, 1])
        with g1:
            st.subheader("Tendencia de Distribución")
            num_cols = df.select_dtypes(include=np.number).columns
            if len(num_cols) > 0:
                fig = px.area(df, y=num_cols[0], color_discrete_sequence=['#3B82F6'], template="plotly_white")
                fig.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with g2:
            st.subheader("Composición")
            fig_pie = px.pie(df, names=df.columns[0], hole=0.6, color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_pie.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=350, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

    elif menu == "Auditoría de Datos":
        st.title("Centro de Auditoría")
        st.dataframe(df.describe(), use_container_width=True)

else:
    st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
    st.columns([1, 2, 1])[1].info("Sincronice un archivo de datos para activar el panel de control.")
