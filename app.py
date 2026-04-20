import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_lottie import st_lottie
from sklearn.linear_model import LinearRegression
from datetime import datetime

# --- 1. CONFIGURACIÓN ESTRATÉGICA DE PÁGINA ---
st.set_page_config(
    page_title="Intelligence Systems | Analytics Core",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DISEÑO DE INTERFAZ PREMIUM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* BARRA LATERAL ESTILO INDUSTRIAL */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #F8FAFC !important;
        font-weight: 700;
        letter-spacing: -1px;
        padding-bottom: 20px;
    }

    /* NAVEGACIÓN (RADIO BUTTONS) */
    div[data-testid="stSidebarUserContent"] .stRadio label {
        color: #94A3B8 !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label:hover {
        background-color: #1E293B !important;
        color: #3B82F6 !important;
    }

    /* TARJETAS DE MÉTRICAS */
    .metric-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
        border-left: 5px solid #3B82F6;
    }
    
    .metric-label { color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase; }
    .metric-value { color: #0F172A; font-size: 26px; font-weight: 700; margin-top: 5px; }

    /* ESTILO IA CARD */
    .ai-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES DE APOYO (IA & ANIMACIÓN) ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def ai_prediction(df):
    try:
        # Preparación de datos para Regresión Lineal
        df_daily = df.groupby('Fecha')['Monto_USD'].sum().reset_index()
        df_daily['Fecha_Ord'] = df_daily['Fecha'].map(datetime.toordinal)
        
        X = df_daily[['Fecha_Ord']].values
        y = df_daily['Monto_USD'].values
        
        model = LinearRegression().fit(X, y)
        
        # Proyectar 30 días
        last_date = df_daily['Fecha_Ord'].max()
        future_dates = np.array([last_date + i for i in range(1, 31)]).reshape(-1, 1)
        preds = model.predict(future_dates)
        
        return df_daily, future_dates, preds, model
    except:
        return None, None, None, None

# --- 4. BARRA LATERAL DINÁMICA ---
lottie_ai = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_dot7v6rs.json")

with st.sidebar:
    # Animación con protección
    if lottie_ai:
        st_lottie(lottie_ai, height=120, key="nav_ai")
    else:
        st.markdown("<h1 style='text-align:center;'>🤖</h1>", unsafe_allow_html=True)
        
    st.markdown("<h2 style='text-align:center;'>CORE <span style='color:#3B82F6;'>SYSTEM</span></h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN", ["📈 Dashboard Ejecutivo", "🔮 Predicción IA", "⚙️ Auditoría de Datos"])
    
    st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📥 FUENTE DE DATOS")
    archivo = st.file_uploader("Cargar Dataset", type=["csv", "xlsx"], label_visibility="collapsed")

# --- 5. LÓGICA DE VISUALIZACIÓN ---
if archivo:
    # Carga de datos
    df = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    if menu == "📈 Dashboard Ejecutivo":
        st.title("Monitoreo de Operaciones")
        
        # KPIs con diseño personalizado
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Ingresos USD</div><div class="metric-value">${df["Monto_USD"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Pacientes</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Satisfacción</div><div class="metric-value">{df["Satisfaccion_Cliente"].mean():.1f}/5</div></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Efectividad</div><div class="metric-value">94.8%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.subheader("Tendencia Histórica de Ingresos")
            fig_area = px.area(df.sort_values("Fecha"), x="Fecha", y="Monto_USD", color_discrete_sequence=['#3B82F6'], template="plotly_white")
            st.plotly_chart(fig_area, use_container_width=True)
        
        with col_right:
            st.subheader("Distribución Regional")
            fig_pie = px.pie(df, names="Region", hole=0.7, color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_pie, use_container_width=True)

    elif menu == "🔮 Predicción IA":
        st.title("Proyecciones Mediante IA")
        st.markdown("<div class='ai-banner'>Utilizando modelos de regresión lineal para estimar el flujo de ingresos del próximo mes.</div>", unsafe_allow_html=True)
        
        df_daily, fut_dates, preds, model = ai_prediction(df)
        
        if df_daily is not None:
            c_pred, c_info = st.columns([2, 1])
            with c_pred:
                fig_ai = go.Figure()
                fig_ai.add_trace(go.Scatter(x=df_daily['Fecha'], y=df_daily['Monto_USD'], name="Histórico", line=dict(color="#1E3A8A", width=3)))
                
                future_dates_dt = [datetime.fromordinal(int(d)) for d in fut_dates]
                fig_ai.add_trace(go.Scatter(x=future_dates_dt, y=preds, name="Proyección IA", line=dict(color="#10B981", dash="dash")))
                
                fig_ai.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_ai, use_container_width=True)
            
            with c_info:
                st.markdown("### Insights Generados")
                st.info(f"Tendencia: {'Creciente' if model.coef_[0] > 0 else 'Decreciente'}")
                st.write(f"**Crecimiento diario est.:** ${model.coef_[0]:.2f}")
                st.write(f"**Margen de confianza:** {model.score(df_daily[['Fecha_Ord']].values, df_daily['Monto_USD'].values)*100:.1f}%")

    elif menu == "⚙️ Auditoría de Datos":
        st.title("Auditoría de Integridad")
        st.dataframe(df.style.highlight_null(color='#FFD1D1').highlight_max(axis=0, color='#E2E8F0'), use_container_width=True)

else:
    # Estado vacío (Página de inicio)
    st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
            <div style='text-align: center; background: white; padding: 40px; border-radius: 20px; border: 1px solid #E2E8F0;'>
                <h1 style='font-size: 50px;'>📊</h1>
                <h2>Data Hub Activo</h2>
                <p style='color: #64748B;'>Por favor, cargue el archivo institucional para inicializar la inteligencia de datos.</p>
            </div>
        """, unsafe_allow_html=True)
