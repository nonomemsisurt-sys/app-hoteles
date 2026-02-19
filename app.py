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
            # Usamos engine='openpyxl' para evitar errores de lectura
            df = pd.read_excel(arc, engine='openpyxl')
            lista_platos = df.stack().dropna().astype(str).tolist()
            # Limpiamos los nombres de los platos
            base_datos_platos.extend([p.strip() for p in lista_platos if len(p) > 4 and "Unnamed" not in p])
        except Exception as e:
            st.error(f"Error leyendo {arc.name}: Revisa que sea un Excel válido.")

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
