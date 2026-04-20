import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración extendida
st.set_page_config(page_title="Data Quality Pro", layout="wide")

st.title("🚀 Dashboard Inteligente de Calidad de Datos")
st.markdown("Analiza, limpia y explora la salud de tus datos de forma interactiva.")

archivo = st.file_uploader("Sube tu archivo CSV o Excel", type=["csv", "xlsx"])

if archivo:
    # 1. Carga de datos con caché para velocidad
    @st.cache_data
    def load_data(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        return pd.read_excel(file)

    df = load_data(archivo)
    
    # --- BARRA LATERAL: HERRAMIENTAS DE LIMPIEZA ---
    st.sidebar.header("🛠️ Acciones de Limpieza")
    if st.sidebar.button("Eliminar Duplicados"):
        df = df.drop_duplicates()
        st.sidebar.success("¡Duplicados eliminados!")

    if st.sidebar.button("Eliminar Filas con Nulos"):
        df = df.dropna()
        st.sidebar.success("¡Nulos eliminados!")

    # --- CÁLCULO DE MÉTRICAS ---
    filas, columnas = df.shape
    nulos = df.isnull().sum().sum()
    total_celdas = filas * columnas
    porcentaje_nulos = (nulos / total_celdas) * 100 if total_celdas > 0 else 0
    duplicados = df.duplicated().sum()
    
    # Score de calidad dinámico
    score = 100 - (porcentaje_nulos + (duplicados/filas*100 if filas > 0 else 0))
    score = max(min(score, 100), 0)

    # --- INTERFAZ POR PESTAÑAS ---
    tab1, tab2, tab3 = st.tabs(["📊 Resumen General", "🔍 Análisis de Calidad", "📈 Exploración Variable"])

    with tab1:
        st.subheader("Indicadores Clave (KPIs)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Filas", filas)
        c2.metric("Total Columnas", columnas)
        c3.metric("% Nulos", f"{porcentaje_nulos:.1f}%")
        c4.metric("Calidad Global", f"{score:.1f}/100")

        st.subheader("Vista Previa de los Datos")
        st.dataframe(df.head(10), use_container_width=True)

    with tab2:
        st.subheader("Análisis Profundo de Integridad")
        col_a, col_b = st.columns(2)

        with col_a:
            # Gráfico de nulos por columna
            nulos_col = df.isnull().sum().reset_index()
            nulos_col.columns = ["Columna", "Cantidad"]
            fig_nulos = px.bar(nulos_col, x="Columna", y="Cantidad", 
                             title="Huecos de información por columna",
                             color="Cantidad", color_continuous_scale="Reds")
            st.plotly_chart(fig_nulos, use_container_width=True)

        with col_b:
            # Tipos de datos
            tipos = df.dtypes.value_counts().reset_index()
            tipos.columns = ["Tipo", "Conteo"]
            fig_tipos = px.pie(tipos, values="Conteo", names="Tipo", title="Distribución de tipos de datos")
            st.plotly_chart(fig_tipos, use_container_width=True)

    with tab3:
        st.subheader("Análisis Estadístico e Interactivo")
        columnas_num = df.select_dtypes(include=np.number).columns.tolist()

        if columnas_num:
            col_sel = st.selectbox("Selecciona una variable para analizar:", columnas_num)
            
            c_graf1, c_graf2 = st.columns(2)
            
            with c_graf1:
                # Histograma dinámico
                fig_hist = px.histogram(df, x=col_sel, marginal="box", 
                                      title=f"Distribución y Outliers de {col_sel}",
                                      color_discrete_sequence=['#636EFA'])
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with c_graf2:
                # Matriz de Correlación
                if len(columnas_num) > 1:
                    corr = df[columnas_num].corr()
                    fig_corr = px.imshow(corr, text_auto=True, title="Mapa de Calor: Correlaciones",
                                       color_continuous_scale="RdBu_r")
                    st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.warning("No se detectaron columnas numéricas para este análisis.")

    # --- BOTÓN DE DESCARGA ---
    st.sidebar.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("📥 Descargar Datos Limpios", data=csv, file_name="datos_procesados.csv", mime="text/csv")
