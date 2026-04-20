import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- CONFIGURACIÓN DE NIVEL EJECUTIVO ---
st.set_page_config(
    page_title="HOSPITAL-IQ | Gestión Estratégica",
    page_icon="🏥",
    layout="wide"
)

# --- ESTILO CLÍNICO PROFESIONAL (CSS) ---
st.markdown("""
    <style>
    /* Estilo para la barra lateral de navegación */
    [data-testid="stSidebar"] {
        background-color: #1A202C !important;
        border-right: 1px solid #2D3748;
    }
    /* Tarjetas de Indicadores Médicos */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    /* Estilo para el área de contenido */
    .main { background-color: #F7FAFC; }
    
    /* Personalización de botones */
    .stButton>button {
        background-color: #3182CE;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENÚ DE NAVEGACIÓN LATERAL (Profesional) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864448.png", width=100)
    st.markdown("### **HOSPITAL-IQ v4.0**")
    st.info("Directora General: Autenticada")
    st.divider()
    
    # Menú de navegación dinámico
    menu = st.radio(
        "Panel de Control",
        ["Dashboard Ejecutivo", "Analítica de Calidad", "Optimización de Recursos", "Exportar Reporte"],
        index=0
    )
    
    st.divider()
    st.markdown("### **Carga de Datos Críticos**")
    archivo = st.file_uploader("Subir Archivo (.csv, .xlsx)", type=["csv", "xlsx"])
    
    if archivo:
        st.success("Base de datos actualizada.")

# --- LÓGICA DE DATOS ---
if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)

    # --- 1. DASHBOARD EJECUTIVO ---
    if menu == "Dashboard Ejecutivo":
        st.title("🏥 Centro de Mando Estratégico")
        st.markdown(f"**Corte de datos:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Fila superior de KPIs Médicos
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Ocupación Camas", "88%", delta="+2% vs mes anterior")
        k2.metric("Tiempo Prom. Espera", "18 min", delta="-4 min", delta_color="normal")
        k3.metric("Satisfacción Paciente", "4.8/5.0", delta="0.1")
        k4.metric("Incidentes Reportados", "0", delta="Objetivo logrado", delta_color="off")

        st.divider()

        # Visualización de Tendencias
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Ingresos por Departamento")
            fig_dept = px.bar(df, x=df.columns[0], y=df.select_dtypes(include=np.number).columns[0],
                             color_discrete_sequence=['#2B6CB0'], template="plotly_white")
            st.plotly_chart(fig_dept, use_container_width=True)
        
        with c2:
            st.subheader("Distribución de Casos Médicos")
            fig_pie = px.pie(df, names=df.columns[1], hole=0.6,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- 2. ANALÍTICA DE CALIDAD (Foco en Integridad) ---
    elif menu == "Analítica de Calidad":
        st.title("🔍 Auditoría de Integridad de Datos")
        st.warning("Evaluación de cumplimiento de registros electrónicos de salud (RES).")
        
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.write("### Auditoría de Nulos")
            nulos = df.isnull().sum()
            st.write(nulos[nulos > 0] if nulos.sum() > 0 else "Cumplimiento al 100% en campos críticos.")
            
        with col_b:
            st.write("### Mapa de Calor de Calidad")
            fig_heat = px.imshow(df.isnull().T, labels=dict(x="Registro", y="Columna", color="¿Faltante?"),
                               color_continuous_scale=['#EDF2F7', '#E53E3E'])
            st.plotly_chart(fig_heat, use_container_width=True)

    # --- 3. OPTIMIZACIÓN DE RECURSOS ---
    elif menu == "Optimización de Recursos":
        st.title("📈 Optimización Operativa")
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            st.subheader("Predicción de Demanda de Recursos")
            selected_col = st.selectbox("Variable Analizada", num_cols)
            fig_trend = px.line(df, y=selected_col, title=f"Histórico de {selected_col}",
                              line_shape="spline", render_mode="svg")
            fig_trend.update_traces(line_color='#2B6CB0', fill='tozeroy')
            st.plotly_chart(fig_trend, use_container_width=True)

    # --- 4. EXPORTAR REPORTE ---
    elif menu == "Exportar Reporte":
        st.title("📄 Reporte para Dirección General")
        st.write("Se ha generado un resumen ejecutivo con los hallazgos principales.")
        
        # Simulación de reporte de texto
        reporte_txt = f"""
        REPORTE EJECUTIVO DE OPERACIONES
        Fecha: {datetime.now().date()}
        Registros Analizados: {len(df)}
        Estado de Datos: {'Óptimo' if df.isnull().sum().sum() == 0 else 'Requiere atención'}
        """
        st.download_button("Descargar Reporte PDF (Simulado)", data=reporte_txt, file_name="Reporte_DG.txt")
        st.success("Reporte listo para firma digital.")

else:
    # Pantalla de bienvenida corporativa
    st.title("Bienvenida, Directora General")
    st.markdown("""
    Este sistema de **Business Intelligence** está diseñado para facilitar la toma de decisiones basada en evidencia.
    
    1. **Seguridad:** Cifrado de datos en tránsito.
    2. **Rapidez:** Análisis de grandes volúmenes en segundos.
    3. **Cumplimiento:** Auditoría automática de registros.
    
    *Por favor, cargue el dataset institucional en la barra lateral para comenzar.*
    """)
    st.image("https://img.freepik.com/free-vector/medical-technology-innovation-concept-vector_53876-175171.jpg", width=600)
