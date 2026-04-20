import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard Inteligente de Calidad de Datos")

archivo = st.file_uploader("Sube tu archivo CSV o Excel", type=["csv", "xlsx"])

if archivo:
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    st.subheader("Vista previa")
    st.dataframe(df.head())

    # Métricas
    filas, columnas = df.shape
    nulos = df.isnull().sum().sum()
    total = filas * columnas
    porcentaje_nulos = (nulos / total) * 100 if total > 0 else 0
    duplicados = df.duplicated().sum()
    porcentaje_duplicados = (duplicados / filas) * 100 if filas > 0 else 0

    st.subheader("Indicadores")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Filas", filas)
    col2.metric("Columnas", columnas)
    col3.metric("% Nulos", f"{porcentaje_nulos:.2f}%")
    col4.metric("% Duplicados", f"{porcentaje_duplicados:.2f}%")

    # Score
    score = 100 - porcentaje_nulos - porcentaje_duplicados
    score = max(score, 0)

    st.subheader("Score de Calidad")
    st.metric("Puntaje", f"{score:.2f}/100")

    # Gráfica de nulos
    nulos_col = df.isnull().sum().reset_index()
    nulos_col.columns = ["Columna", "Nulos"]

    fig = px.bar(nulos_col, x="Columna", y="Nulos", title="Nulos por columna")
    st.plotly_chart(fig)

    # Histograma
    columnas_num = df.select_dtypes(include="number").columns.tolist()

    if columnas_num:
        col_sel = st.selectbox("Selecciona una columna numérica", columnas_num)

        fig2 = px.histogram(df, x=col_sel, title=f"Distribución de {col_sel}")
        st.plotly_chart(fig2)
