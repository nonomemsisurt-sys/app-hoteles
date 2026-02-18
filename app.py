import streamlit as st
import pandas as pd
import random
import requests
import io

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Chef Master - Hoteles", layout="wide")
API_KEY = "5bcf10f5df4c417d8810a97ae971b49c"

if 'secciones' not in st.session_state:
    st.session_state.secciones = ["Carnes", "Pescados", "Plancha", "Showcooking 1", "Showcooking 2", "Ensaladas", "Vegetarianos", "Guarniciones", "Tostas Frías", "Tostas Calientes", "Rincon 1", "Rincón del Pastelero", "Postres Secos", "Pastelería"]

st.title("🏨 Gestor Gastronómico Inteligente")

# --- BARRA LATERAL ---
with st.sidebar:
    hotel = st.selectbox("Seleccione Hotel:", ["Ambar", "Aquamarine", "Turquesa", "Esmeralda", "Punta Cana", "Fantasia"])
    st.divider()
    nueva = st.text_input("Añadir nueva sección:")
    if st.button("➕ Añadir"):
        if nueva and nueva not in st.session_state.secciones:
            st.session_state.secciones.append(nueva)
            st.rerun()

# --- CARGA DE ARCHIVOS ---
st.subheader("1. Sube tus manuales de recetas")
archivos = st.file_uploader("Arrastra tus archivos de Excel (.xlsx)", type=['xlsx'], accept_multiple_files=True)
base_datos_platos = []

if archivos:
    for arc in archivos:
        try:
            df = pd.read_excel(arc)
            # Extraer nombres de platos de todas las celdas
            lista_platos = df.stack().dropna().astype(str).tolist()
            base_datos_platos.extend([p.strip() for p in lista_platos if len(p) > 4 and "Unnamed" not in p])
        except Exception as e:
            st.error(f"Error leyendo {arc.name}")

if base_datos_platos:
    st.success(f"✅ IA: He aprendido {len(base_datos_platos)} platos de tus archivos.")

# --- GENERADOR ---
st.divider()
st.header(f"2. Configurar Rueda - Hotel {hotel}")
col1, col2, col3 = st.columns(3)
with col1:
    dias = st.number_input("Días del ciclo:", 1, 30, 7)
with col2:
    fuente = st.radio("Fuente de platos:", ["Mis Archivos", "Spoonacular (API)", "Mix Inteligente"])
with col3:
    noche = st.selectbox("Noche Temática:", ["Ninguna", "Gala", "Mexicana", "Dominicana", "Asiática", "Italiana"])

# Cantidades
st.write("**Cantidad de platos distintos por sección cada día:**")
cantidades = {}
cols_sec = st.columns(4)
for i, sec in enumerate(st.session_state.secciones):
    cantidades[sec] = cols_sec[i % 4].number_input(f"{sec}:", 1, 10, 2)

if st.button("🚀 GENERAR MENÚ COMPLETO"):
    if fuente == "Mis Archivos" and not base_datos_platos:
        st.error("❌ Sube archivos Excel primero.")
    else:
        with st.spinner("La IA está organizando el buffet..."):
            resultado = []
            for d in range(1, dias + 1):
                fila = {"Dia": f"Dia {d}"}
                for sec in st.session_state.secciones:
                    platos_dia = []
                    for _ in range(cantidades[sec]):
                        if fuente == "Mis Archivos":
                            plato = random.choice(base_datos_platos) if base_datos_platos else "Revisar Manual"
                        elif fuente == "Spoonacular (API)":
                            try:
                                q = f"{sec} {noche}" if noche != "Ninguna" else sec
                                res = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?query={q}&number=10&apiKey={API_KEY}").json()
                                plato = random.choice(res['results'])['title']
                            except:
                                plato = f"Sugerencia {sec}"
                        else: # Mix
                            if base_datos_platos and random.random() > 0.5:
                                plato = random.choice(base_datos_platos)
                            else:
                                plato = f"Idea Chef {sec}"
                        platos_dia.append(plato)
                    fila[sec] = " / ".join(platos_dia)
                resultado.append(fila)
            
            df_final = pd.DataFrame(resultado)
            st.dataframe(df_final)
            
            # EXPORTACIÓN OPTIMIZADA (Punto y coma para Excel español)
            csv = df_final.to_csv(index=False, sep=';').encode('utf-8-sig')
            st.download_button("📥 Descargar Menú para EXCEL", csv, f"Menu_{hotel}.csv", "text/csv")
