import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
from streamlit_lottie import st_lottie
from sklearn.linear_model import LinearRegression
import datetime as dt  # Importación corregida para evitar NameError

# --- 1. CONFIGURACIÓN ESTRATÉGICA ---
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

    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #F8FAFC !important;
        font-weight: 700;
        letter-spacing: -1px;
    }

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
        # Agrupar por fecha y sumar montos
        df_daily = df.groupby('Fecha')['Monto_USD'].sum().reset_index()
        # CORRECCIÓN AQUÍ: Usamos dt.datetime.toordinal
        df_daily['Fecha_Ord'] = df_daily['Fecha'].apply(lambda x: x.toordinal())
        
        X = df_daily[['Fecha_Ord']].values
        y = df_daily['Monto_USD'].values
        
        model = LinearRegression().fit(X, y)
        
        # Proyectar 30 días futuros
        last_date_ord = df_daily['Fecha_Ord'].max()
        future_dates_ord = np.array([last_date_ord + i for i in range(1, 31)]).reshape(-1, 1)
        preds = model.predict(future_dates_ord)
        
        # Convertir ordinales de vuelta a objetos datetime para graficar
        future_dates_dt = [dt.date.fromordinal(int(d[0])) for d in future_dates_ord]
        
        return df_daily, future_dates_dt, preds, model
    except Exception as e:
        st.error(f"Error en IA: {e}")
        return None, None, None, None

# --- 4. BARRA LATERAL ---
lottie_ai = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_dot7v6rs.json")

with st.sidebar:
    if lottie_ai:
        st_lottie(lottie_ai, height=120, key="nav_ai")
    else:
        st.markdown("<h1 style='text-align:center;'>🤖</h1>", unsafe_allow_html=True)
        
    st.markdown("<h2 style='text-align:center;'>CORE <span style='color:#3B82F6;'>SYSTEM</span></h2>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("NAVEGACIÓN", ["📈 Dashboard Ejecutivo", "🔮 Predicción IA", "⚙️ Auditoría de Datos"])
    
    st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
    archivo = st.file_uploader("Cargar Dataset", type=["csv", "xlsx"])

# --- 5. LÓGICA DE VISUALIZACIÓN ---
if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith('.csv') else pd.read_excel(archivo)
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    if menu == "📈 Dashboard Ejecutivo":
        st.title("Monitoreo de Operaciones")
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f'<div class="metric-card"><div class="metric-label">Ingresos USD</div><div class="metric-value">${df["Monto_USD"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="metric-card"><div class="metric-label">Registros</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="metric-card"><div class="metric-label">Satisfacción</div><div class="metric-value">{df["Satisfaccion_Cliente"].mean():.1f}/5</div></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="metric-card"><div class="metric-label">Efectividad</div><div class="metric-value">94.8%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        c_left, c_right = st.columns([2, 1])
        with c_left:
            fig_area = px.area(df.sort_values("Fecha"), x="Fecha", y="Monto_USD", 
                               title="Evolución de Ingresos", color_discrete_sequence=['#3B82F6'], template="plotly_white")
            st.plotly_chart(fig_area, use_container_width=True)
        with c_right:
            fig_pie = px.pie(df, names="Region", hole=0.7, title="Distribución Regional",
                            color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_pie, use_container_width=True)

    elif menu == "🔮 Predicción IA":
        st.title("Proyecciones Mediante IA")
        st.markdown("<div class='ai-banner'>Modelo de Regresión Lineal entrenado para estimar el flujo del próximo mes.</div>", unsafe_allow_html=True)
        
        df_daily, fut_dates, preds, model = ai_prediction(df)
        
        if df_daily is not None:
            c_p, c_i = st.columns([2, 1])
            with c_p:
                fig_ai = go.Figure()
                fig_ai.add_trace(go.Scatter(x=df_daily['Fecha'], y=df_daily['Monto_USD'], name="Histórico", line=dict(color="#1E3A8A", width=3)))
                fig_ai.add_trace(go.Scatter(x=fut_dates, y=preds, name="Proyección IA", line=dict(color="#10B981", dash="dash")))
                fig_ai.update_layout(template="plotly_white", xaxis_title="Tiempo", yaxis_title="USD")
                st.plotly_chart(fig_ai, use_container_width=True)
            with c_i:
                st.subheader("Insights IA")
                st.info(f"Tendencia: {'Creciente' if model.coef_[0] > 0 else 'Decreciente'}")
                st.write(f"**Crecimiento diario est.:** ${model.coef_[0]:.2f}")
                st.write(f"**Confianza (R²):** {model.score(df_daily[['Fecha_Ord']].values, df_daily['Monto_USD'].values)*100:.1f}%")

    elif menu == "⚙️ Auditoría de Datos":
        st.title("Auditoría de Integridad")
        st.dataframe(df.style.highlight_null(color='#FFD1D1'), use_container_width=True)

else:
    st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
    st.columns([1, 2, 1])[1].info("Sistema en espera. Por favor, cargue el dataset institucional.")
