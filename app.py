import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Data Insights | Enterprise Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS AVANZADO ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Títulos y Subtítulos */
    h1, h2, h3 {
        color: #1E293B !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* Tabs profesionales */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #64748B;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #0F172A !important;
        border-bottom: 2px solid #3B82F6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE CÓMPUTO ---
@st.cache_data
def process_data(file):
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    # Limpieza básica automática de nombres de columnas
    df.columns = [c.strip().replace(' ', '_') for c in df.columns]
    return df

def calculate_outliers(series):
    z_scores = (series - series.mean()) / series.std()
    return np.abs(z_scores) > 3

# --- UI - BARRA LATERAL ---
with st.sidebar:
    st.title("⚙️ Engine")
    uploaded_file = st.file_uploader("Cargar Dataset", type=["csv", "xlsx"])
    st.divider()
    if uploaded_file:
        st.success("Dataset Conectado")
        mode = st.radio("Enfoque del Análisis", ["Calidad de Datos", "Estadística Pro", "Relaciones"])

# --- UI - CONTENIDO PRINCIPAL ---
if uploaded_file:
    df = process_data(uploaded_file)
    
    # Header Principal
    st.title("Analytics Command Center")
    st.info("Visualizando la integridad y salud de la infraestructura de datos.")

    # --- MÉTRICAS KPI (Estilo Dashboard Ejecutivo) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Registros Totales", f"{len(df):,}")
    with col2:
        nulos = df.isnull().sum().sum()
        st.metric("Integridad (Nulos)", f"{nulos}", delta=f"{(nulos/df.size)*100:.1f}%", delta_color="inverse")
    with col3:
        num_cols = df.select_dtypes(include=np.number).columns
        anomalias = sum([calculate_outliers(df[col]).sum() for col in num_cols]) if len(num_cols) > 0 else 0
        st.metric("Anomalías Detectadas", int(anomalias), delta="Z-Score > 3")
    with col4:
        st.metric("Dimensión del Dataframe", f"{df.shape[1]} Col")

    st.markdown("---")

    # --- PESTAÑAS DE ANÁLISIS ---
    t1, t2, t3 = st.tabs(["📊 Perfilado", "🔍 Deep Analysis", "🗄️ RAW Explorer"])

    with t1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            st.subheader("Salud por Atributo")
            missing_df = df.isnull().sum().reset_index()
            missing_df.columns = ['Columna', 'Faltantes']
            fig_missing = px.bar(
                missing_df, x='Faltantes', y='Columna', orientation='h',
                color='Faltantes', color_continuous_scale='Blues',
                template='simple_white'
            )
            fig_missing.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_missing, use_container_width=True)

        with c2:
            st.subheader("Composición de Datos")
            dtypes_df = df.dtypes.value_counts().reset_index()
            dtypes_df.columns = ['Tipo', 'Conteo']
            fig_pie = px.pie(
                dtypes_df, values='Conteo', names='Tipo',
                hole=0.5, color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with t2:
        if len(num_cols) > 0:
            target_col = st.selectbox("Seleccionar Variable para Análisis Profundo", num_cols)
            
            sub_c1, sub_c2 = st.columns(2)
            with sub_c1:
                # Boxplot Profesional
                fig_box = px.box(df, y=target_col, points="all", 
                                title=f"Distribución y Outliers: {target_col}",
                                color_discrete_sequence=['#0F172A'])
                st.plotly_chart(fig_box, use_container_width=True)
            
            with sub_c2:
                # ECDF (Función de distribución acumulada) - Muy pro para estadística
                fig_ecdf = px.ecdf(df, x=target_col, title=f"Curva de Probabilidad Acumulada")
                st.plotly_chart(fig_ecdf, use_container_width=True)
        else:
            st.warning("No hay datos numéricos para análisis profundo.")

    with t3:
        st.subheader("Data Explorer (Filtrado)")
        # Buscador dinámico
        search = st.text_input("Filtrar registros por texto...")
        if search:
            mask = df.apply(lambda x: x.astype(str).str.contains(search, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

else:
    # Estado de espera
    st.empty()
    col_empty, col_msg = st.columns([1, 2])
    with col_msg:
        st.title("Bienvenido al Command Center")
        st.write("Carga un archivo en el panel izquierdo para desplegar la inteligencia de negocio.")
        st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-8041.jpg", width=400)
