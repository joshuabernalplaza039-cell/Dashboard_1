import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="HOSPITAL-IQ | Intelligence Hub", layout="wide", page_icon="🏥")

# 2. ESTILO CSS (SideBar Midnight & Data Cards)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0F172A !important; }
    [data-testid="stSidebar"] * { color: #94A3B8 !important; }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    h1, h2, h3 { color: #1E293B; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL DINÁMICA
with st.sidebar:
    st.markdown("<h2 style='color: white;'>CORE <span style='color: #3B82F6;'>ANALYTICS</span></h2>", unsafe_allow_html=True)
    st.divider()
    
    modulo = st.selectbox("MÓDULO DE TRABAJO", ["📊 Dashboard Operativo", "🧪 Análisis de Calidad", "📦 Explorador de Datos"])
    
    st.divider()
    archivo = st.file_uploader("Cargar Base de Datos", type=["csv"])

# 4. PROCESAMIENTO Y GRÁFICAS
if archivo:
    df = pd.read_csv(archivo)
    df['Fecha'] = pd.to_datetime(df['Fecha']) # Asegurar formato fecha

    if modulo == "📊 Dashboard Operativo":
        st.title("Monitoreo de Gestión Hospitalaria")
        
        # KPIs Superiores
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ingresos Totales", f"${df['Monto_USD'].sum():,.0f}", "+4.2%")
        c2.metric("Ticket Promedio", f"${df['Monto_USD'].mean():,.2f}")
        c3.metric("Satisfacción", f"{df['Satisfaccion_Cliente'].mean():.1f} / 5.0")
        c4.metric("Tasa de Error", f"{(df['Estado_Pago'] == 'Error').mean()*100:.1f}%", "-1.2%", delta_color="inverse")

        st.markdown("---")

        # FILA 1: TENDENCIA TEMPORAL Y REGIONES
        g1, g2 = st.columns([2, 1])
        
        with g1:
            st.subheader("Evolución de Ingresos Mensuales")
            df_time = df.set_index('Fecha').resample('M')['Monto_USD'].sum().reset_index()
            fig_line = px.area(df_time, x='Fecha', y='Monto_USD', 
                              line_shape='spline',
                              color_discrete_sequence=['#3B82F6'])
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_line, use_container_width=True)

        with g2:
            st.subheader("Distribución por Región")
            fig_pie = px.pie(df, names='Region', hole=0.6,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

        # FILA 2: ESTADO DE PAGO Y DISPERSIÓN
        g3, g4 = st.columns(2)
        
        with g3:
            st.subheader("Estado de Transacciones por Cliente")
            fig_bar = px.bar(df, x='Cliente', color='Estado_Pago', 
                            barmode='group',
                            color_discrete_map={'Completado':'#10B981', 'Pendiente':'#F59E0B', 'Error':'#EF4444', 'Cancelado':'#64748B'})
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with g4:
            st.subheader("Relación Monto vs Satisfacción")
            fig_scatter = px.scatter(df, x='Monto_USD', y='Satisfaccion_Cliente', 
                                    color='Region', size='Costo_Envio',
                                    hover_name='ID_Transaccion',
                                    color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_scatter, use_container_width=True)

    elif modulo == "🧪 Análisis de Calidad":
        st.title("Diagnóstico de Integridad del Dataset")
        
        col_err1, col_err2 = st.columns(2)
        
        with col_err1:
            st.write("### Nulos por Atributo")
            nulos = df.isnull().sum().reset_index()
            nulos.columns = ['Campo', 'Faltantes']
            fig_n = px.bar(nulos[nulos['Faltantes']>0], x='Campo', y='Faltantes', color_discrete_sequence=['#EF4444'])
            st.plotly_chart(fig_n, use_container_width=True)
            
        with col_err2:
            st.write("### Detección de Outliers (Z-Score)")
            fig_box = px.box(df, y='Monto_USD', points="outliers", color_discrete_sequence=['#1E3A8A'])
            st.plotly_chart(fig_box, use_container_width=True)

    elif modulo == "📦 Explorador de Datos":
        st.title("Explorador de Registros")
        reg_sel = st.multiselect("Filtrar por Región:", df['Region'].unique())
        if reg_sel:
            df = df[df['Region'].isin(reg_sel)]
        st.dataframe(df.style.highlight_null(color='#FFD1D1'), use_container_width=True)

else:
    st.info("👋 Bienvenue. Por favor, cargue el archivo 'dataset_calidad_profesional.csv' para activar las gráficas.")
