import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE MARCA Y ESTILO
st.set_page_config(page_title="Data Insights Pro", layout="wide", page_icon="🔵")

# CSS inyectado para mejorar la estética (Azules Profesionales)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #003366;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] {
        background-color: #001529;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040523.png", width=80)
    st.title("Data Engine")
    st.info("Sube tu dataset para iniciar el diagnóstico de calidad.")
    archivo = st.file_uploader("Cargar Archivo", type=["csv", "xlsx"])
    
    if archivo:
        st.success("Archivo cargado con éxito")
        st.divider()
        st.markdown("### Configuración de Visualización")
        tema_azul = st.select_slider("Intensidad de color", options=["Light", "Sky", "Navy"])

# 3. LÓGICA DE DATOS
if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
    
    # Cálculos Pro
    filas, columnas = df.shape
    nulos_totales = df.isnull().sum().sum()
    pct_nulos = (nulos_totales / (filas * columnas)) * 100
    
    # 4. HEADER Y KPIs
    st.title("🔵 Business Intelligence Dashboard")
    st.markdown("---")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Registros Totales", f"{filas:,}")
    m2.metric("Dimensiones", f"{columnas} col")
    m3.metric("Health Score", f"{100 - pct_nulos:.1f}%", delta=f"{-pct_nulos:.1f}%", delta_color="inverse")
    m4.metric("Duplicados", f"{df.duplicated().sum()}")

    # 5. LAYOUT PRINCIPAL (Tabs con diseño limpio)
    tab_data, tab_viz, tab_report = st.tabs(["📋 Explorador", "📈 Análisis Visual", "⚙️ Integridad"])

    with tab_data:
        st.subheader("Estructura del Dataset")
        st.dataframe(df.head(20), use_container_width=True)

    with tab_viz:
        c1, c2 = st.columns([1, 1])
        
        num_cols = df.select_dtypes(include="number").columns.tolist()
        
        if num_cols:
            with c1:
                # Histograma en Tonos Azules
                col_x = st.selectbox("Eje X (Distribución)", num_cols)
                fig_hist = px.histogram(df, x=col_x, 
                                      color_discrete_sequence=['#003366'],
                                      template="plotly_white",
                                      title=f"Distribución de {col_x}")
                st.plotly_chart(fig_hist, use_container_width=True)
                
            with c2:
                # Scatter Plot (Relación)
                if len(num_cols) > 1:
                    col_y = st.selectbox("Eje Y (Relación)", num_cols, index=1)
                    fig_scat = px.scatter(df, x=col_x, y=col_y, 
                                        color_discrete_sequence=['#1f77b4'],
                                        template="plotly_white",
                                        title="Correlación entre Variables")
                    st.plotly_chart(fig_scat, use_container_width=True)

    with tab_report:
        st.subheader("Mapa de Calor de Datos Faltantes")
        # Gráfico de barras de nulos estilizado
        nulos_data = df.isnull().sum().reset_index()
        nulos_data.columns = ["Columna", "Faltantes"]
        
        fig_nulos = px.bar(nulos_data, x="Faltantes", y="Columna", 
                         orientation='h',
                         color="Faltantes",
                         color_continuous_scale=["#e0f3f8", "#084594"],
                         title="Nulos por Variable")
        st.plotly_chart(fig_nulos, use_container_width=True)

else:
    st.warning("👈 Por favor, sube un archivo en la barra lateral para comenzar.")
