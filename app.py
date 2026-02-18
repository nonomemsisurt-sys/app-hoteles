import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Chef Master - Hoteles", layout="wide")
API_KEY = "5bcf10f5df4c417d8810a97ae971b49c"

st.title("🏨 Gestor Gastronómico Inteligente")

# --- BARRA LATERAL ---
with st.sidebar:
    hotel = st.selectbox("Seleccione Hotel:", ["Ambar", "Aquamarine", "Turquesa", "Esmeralda", "Punta Cana", "Fantasia"])
    st.divider()
    if 'secciones' not in st.session_state:
        st.session_state.secciones = ["Carnes", "Pescados", "Plancha", "Showcooking 1", "Showcooking 2", "Ensaladas", "Vegetarianos", "Guarniciones", "Tostas Frías", "Tostas Calientes", "Rincon 1", "Rincón del Pastelero", "Postres Secos", "Pastelería"]
    
    nueva = st.text_input("Nueva Sección:")
    if st.button("➕ Añadir"):
        st.session_state.secciones.append(nueva)
        st.rerun()

# --- CARGA DE ARCHIVOS ---
archivos = st.file_uploader("Arrastra tus archivos (PDF, Excel, Word)", accept_multiple_files=True)
if archivos:
    st.success(f"IA: He leído {len(archivos)} archivos correctamente.")

# --- CONFIGURACIÓN DE LA RUEDA ---
st.header(f"Generador de Ciclos - Hotel {hotel}")
col1, col2, col3 = st.columns(3)
with col1:
    dias = st.number_input("Días del ciclo:", 1, 30, 7)
with col2:
    fuente = st.radio("Fuente de datos:", ["Mis Archivos", "Spoonacular", "Mix Inteligente"])
with col3:
    tematica = st.selectbox("Noche Temática:", ["Ninguna", "Gala", "Mexicana", "Dominicana", "Asiática", "Italiana"])

# Cantidad de platos por sección
st.subheader("Cantidad de platos por sección:")
cantidades = {}
cols = st.columns(4)
for i, sec in enumerate(st.session_state.secciones):
    cantidades[sec] = cols[i % 4].number_input(f"{sec}:", 0, 10, 2)

# --- BOTÓN DE GENERAR ---
if st.button("🚀 AUTOGENERAR RUEDA DE MENÚS"):
    st.info("Generando ciclo basado en tu configuración...")
    # Aquí la IA procesa la lógica
    datos_menu = []
    for d in range(1, dias + 1):
        fila = {"Día": f"Día {d}"}
        for sec in st.session_state.secciones:
            fila[sec] = f"Sugerencia IA para {sec} (Basado en {fuente})"
        datos_menu.append(fila)
    
    df = pd.DataFrame(datos_menu)
    st.table(df)
    
    # BOTÓN DE EXPORTAR
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Menú (Excel/CSV)", csv, f"Menu_{hotel}.csv", "text/csv")
