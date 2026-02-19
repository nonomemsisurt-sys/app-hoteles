import streamlit as st
import pandas as pd
import random
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Chef Master - Hoteles", layout="wide")
API_KEY = "5bcf10f5df4c417d8810a97ae971b49c"

if 'secciones' not in st.session_state:
    st.session_state.secciones = ["Carnes", "Pescados", "Plancha", "Showcooking 1", "Showcooking 2", "Ensaladas", "Vegetarianos", "Guarniciones", "Tostas Frías", "Tostas Calientes", "Rincon 1", "Rincón del Pastelero", "Postres Secos", "Pastelería"]

st.title("🏨 Gestor Gastronómico Inteligente")

# --- CARGA DE ARCHIVOS ---
st.subheader("1. Sube tus manuales de recetas")
archivos = st.file_uploader("Arrastra tus archivos de Excel (.xlsx)", type=['xlsx'], accept_multiple_files=True)
base_datos_platos = []

if archivos:
    for arc in archivos:
        try:
            df = pd.read_excel(arc, engine='openpyxl')
            # Convertimos todo el Excel en una lista de palabras
            lista_raw = df.stack().dropna().astype(str).tolist()
            
            for p in lista_raw:
                p_limpio = p.strip()
                # FILTRO: Solo guardamos si tiene más de 5 letras 
                # y NO es una palabra de alérgenos o ingredientes sueltos
                palabras_basura = ["Gluten", "Lácteos", "Frutos secos", "Nutella", "Mantequilla", "Pan ", "Unnamed"]
                if len(p_limpio) > 5 and not any(basura in p_limpio for basura in palabras_basura):
                    base_datos_platos.append(p_limpio)
        except Exception as e:
            st.error(f"Error leyendo {arc.name}")

if base_datos_platos:
    # Quitamos duplicados para que no se repitan platos
    base_datos_platos = list(set(base_datos_platos))
    st.success(f"✅ IA: He filtrado y aprendido {len(base_datos_platos)} platos reales.")

if base_datos_platos:
    st.success(f"✅ IA: He aprendido {len(base_datos_platos)} platos de tus archivos.")

# --- GENERADOR ---
st.divider()
st.header(f"2. Configurar Rueda")
col1, col2 = st.columns(2)
with col1:
    dias = st.number_input("Días del ciclo:", 1, 30, 7)
with col2:
    fuente = st.radio("Fuente de platos:", ["Mis Archivos", "Spoonacular (API)", "Mix Inteligente"])

if st.button("🚀 GENERAR MENÚ COMPLETO"):
    if fuente == "Mis Archivos" and not base_datos_platos:
        st.error("❌ Sube archivos primero.")
    else:
        resultado = []
        for d in range(1, dias + 1):
            fila = {"Dia": f"Dia {d}"}
            for sec in st.session_state.secciones:
                if fuente == "Mis Archivos":
                    plato = random.choice(base_datos_platos) if base_datos_platos else "Revisar Manual"
                else:
                    plato = f"Sugerencia Chef {sec}"
                fila[sec] = plato
            resultado.append(fila)
        
        df_final = pd.DataFrame(resultado)
        st.dataframe(df_final)
        
        # Exportación preparada para Excel
        csv = df_final.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button("📥 Descargar para Excel", csv, "Menu_Hoteles.csv", "text/csv")
