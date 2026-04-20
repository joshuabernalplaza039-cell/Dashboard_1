import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_lottie import st_lottie
import requests
from sklearn.linear_model import LinearRegression
import time

## 1. Función de carga segura
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# 2. Cargar las animaciones
lottie_ai = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_dot7v6rs.json")

# 3. Mostrar la animación solo si se cargó correctamente
with st.sidebar:
    if lottie_ai:
        st_lottie(lottie_ai, height=150, key="ai_icon")
    else:
        st.markdown("🤖 **AI Core Active**") # Texto de respaldo si falla el JSON

# 4. BARRA LATERAL
with st.sidebar:
    st_lottie(lottie_ai, height=150, key="ai_icon")
    st.markdown("<h2 style='color: white; text-align: center;'>AI CORE</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("SISTEMA", ["🔮 Predicción IA", "📊 Insight Operativo", "🕵️ Auditoría"])
    archivo = st.file_uploader("Actualizar Dataset", type=["csv"])

# 5. LÓGICA CON IA
if archivo:
    df = pd.read_csv(archivo)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    if menu == "🔮 Predicción IA":
        st.title("Proyección Inteligente de Ingresos")
        
        # --- MODELO DE IA (Regresión Lineal Simple) ---
        # Preparamos los datos: convertir fechas a números ordinales
        df_ai = df.groupby('Fecha')['Monto_USD'].sum().reset_index()
        df_ai['Fecha_Ordinal'] = df_ai['Fecha'].map(datetime.toordinal)
        
        X = df_ai[['Fecha_Ordinal']].values
        y = df_ai['Monto_USD'].values
        
        modelo = LinearRegression()
        modelo.fit(X, y)
        
        # Predecir los próximos 30 días
        ultima_fecha = df_ai['Fecha_Ordinal'].max()
        fechas_futuras = np.array([ultima_fecha + i for i in range(1, 31)]).reshape(-1, 1)
        predicciones = modelo.predict(fechas_futuras)
        
        # Visualización
        st.markdown("""
            <div class='ai-card'>
                <h3>Análisis Predictivo Activado</h3>
                <p>El modelo ha detectado una tendencia de crecimiento basada en los últimos registros.</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=df_ai['Fecha'], y=y, name='Histórico', line=dict(color='#3B82F6')))
            fig_pred.add_trace(go.Scatter(x=[datetime.fromordinal(int(i)) for i in fechas_futuras], 
                                         y=predicciones, name='Predicción IA', line=dict(dash='dash', color='#10B981')))
            st.plotly_chart(fig_pred, use_container_width=True)
            
        with c2:
            st.subheader("Métricas Predictivas")
            st.write(f"**Crecimiento Estimado:** {modelo.coef_[0]:.2f} USD/día")
            st.write(f"**Confianza del Modelo:** {modelo.score(X, y)*100:.1f}%")
            if modelo.coef_[0] > 0:
                st.success("Tendencia Positiva")
            else:
                st.error("Alerta: Tendencia a la baja")

    elif menu == "📊 Insight Operativo":
        st.title("Business Insights")
        # Animación de carga para simular "pensamiento" de IA
        with st.spinner('IA analizando patrones...'):
            time.sleep(1)
            st_lottie(lottie_success, height=100, key="success")
        
        col1, col2 = st.columns(2)
        with col1:
            # Gráfico con animación de Plotly (burbujas animadas)
            fig_anim = px.scatter(df, x="Monto_USD", y="Costo_Envio", 
                                 animation_frame="Region", size="Satisfaccion_Cliente",
                                 color="Estado_Pago", hover_name="ID_Transaccion",
                                 log_x=True, size_max=55, range_x=[100,100000], range_y=[0,60])
            st.plotly_chart(fig_anim, use_container_width=True)
        
        with col2:
            st.subheader("Hallazgos Automáticos")
            st.info(f"💡 La región con mejor desempeño es **{df.groupby('Region')['Monto_USD'].sum().idxmax()}**.")
            st.info(f"💡 Se detectaron **{df.duplicated().sum()}** registros redundantes que afectan la veracidad.")

    elif menu == "🕵️ Auditoría":
        st.title("Auditoría de Datos con Heurística")
        st.dataframe(df.style.background_gradient(subset=['Monto_USD'], cmap='Blues'))

else:
    st.markdown("<div style='text-align: center; margin-top: 100px;'>", unsafe_allow_html=True)
    st_lottie(lottie_ai, height=300)
    st.header("Esperando Dataset para inicializar motores de IA...")
    st.markdown("</div>", unsafe_allow_html=True)
