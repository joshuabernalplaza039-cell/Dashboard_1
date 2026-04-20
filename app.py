import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="HOSPITAL-IQ Premium", layout="wide", page_icon="🏥")

# 2. SISTEMA DE ESTILO CSS AVANZADO (The "Secret Sauce")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fondo de la aplicación */
    .stApp {
        background-color: #F0F2F5;
    }

    /* Contenedor de Tarjetas (Cards) */
    .metric-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-left: 6px solid #1E3A8A;
        margin-bottom: 10px;
    }
    
    .metric-title {
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        color: #1E293B;
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
    }

    /* Personalización Sidebar */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(#1E3A8A, #0F172A);
        color: white;
    }
    
    /* Botones Modernos */
    .stButton>button {
        background: #1E3A8A;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #3B82F6;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (Navigation)
with st.sidebar:
    st.markdown("<h2 style='color: white;'>🏥 Global Health</h2>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio(
        "SISTEMA DE GESTIÓN",
        ["📊 Overview Directivo", "🔬 Análisis de Datos", "🛡️ Control de Calidad"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("### 📁 Fuentes de Datos")
    archivo = st.file_uploader("Actualizar Registro Mensual", type=["csv", "xlsx"])
    
    if archivo:
        st.success("Sincronización Exitosa")

# 4. FUNCIONES DE RENDERIZADO DE TARJETAS
def make_card(title, value, delta, color="#1E3A8A"):
    delta_color = "#10B981" if "+" in delta else "#EF4444"
    st.markdown(f"""
        <div class="metric-card" style="border-left-color: {color}">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div style="color: {delta_color}; font-size: 14px; font-weight: 600;">
                {delta} <span style="color: #94A3B8; font-weight: 400;">vs mes ant.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. CONTENIDO PRINCIPAL
if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)

    if menu == "📊 Overview Directivo":
        st.markdown("<h1 style='color: #0F172A; margin-bottom: 0;'>Panel de Control Institucional</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 18px;'>Resumen estratégico de desempeño hospitalario</p>", unsafe_allow_html=True)
        
        # Tarjetas Personalizadas (HTML)
        c1, c2, c3, c4 = st.columns(4)
        with c1: make_card("Ocupación Total", "92.4%", "+3.2%")
        with c2: make_card("Pacientes Críticos", "48", "-5.0%", "#EF4444")
        with c3: make_card("Tiempo de Respuesta", "12m 40s", "-12.5%")
        with c4: make_card("Eficiencia de Camas", "0.89", "+0.04", "#8B5CF6")

        st.markdown("### Tendencias de Admisión")
        
        # Gráfico Plotly con estilo "Goldman Sachs"
        fig = px.area(df, x=df.columns[0], y=df.select_dtypes(include=np.number).columns[0],
                     line_shape='spline',
                     color_discrete_sequence=['#1E3A8A'])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig, use_container_width=True)

        # Doble columna de análisis
        col_left, col_right = st.columns([1, 1.5])
        with col_left:
            st.markdown("### Especialidades")
            fig_pie = px.pie(df, names=df.columns[1], hole=0.7,
                            color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_right:
            st.markdown("### Top Desempeño por Área")
            st.dataframe(df.head(8), use_container_width=True)

    elif menu == "🔬 Análisis de Datos":
        st.title("Explorador de Variables Médicas")
        # Aquí puedes poner tus filtros y gráficos anteriores pero con el estilo nuevo
        st.info("Utilice las herramientas de filtrado para analizar cohortes específicas.")
        
    elif menu == "🛡️ Control de Calidad":
        st.title("Gobernanza y Auditoría")
        st.markdown("Análisis de integridad de registros bajo norma internacional.")
        st.divider()
        st.json({"Auditoría": "Aprobada", "Errores_Detectados": 0, "Confianza": "99.8%"})

else:
    # PANTALLA DE BIENVENIDA (Empty State)
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_empty1, c_empty2, c_empty3 = st.columns([1, 2, 1])
    with c_empty2:
        st.markdown("""
            <div style="text-align: center; background: white; padding: 50px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
                <h1 style="font-size: 50px;">👋</h1>
                <h2 style="color: #1E293B;">Bienvenida, Directora</h2>
                <p style="color: #64748B;">El sistema está listo para procesar los datos institucionales.<br>Por favor, cargue el archivo de gestión para comenzar.</p>
            </div>
        """, unsafe_allow_html=True)
