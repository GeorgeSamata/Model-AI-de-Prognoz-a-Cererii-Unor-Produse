import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(page_title="SIA Mentenanță Predictivă", layout="wide")
st.title("SIA - Dashboard Mentenanță Predictivă")

@st.cache_resource
def load_resources():
    scaler_path = "data/processed/preprocessor.pkl"
    model_path = "models/untrained_model.pkl"
    
    scaler = None
    model = None
    
    if os.path.exists(scaler_path):
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
    return scaler, model

scaler, model = load_resources()

st.sidebar.header("Panou Control Senzori")

def user_input():
    viteza = st.sidebar.slider("Viteză Operare (%)", 50.0, 100.0, 85.0)
    sarcina = st.sidebar.slider("Sarcină Utilă (kg)", 0.5, 10.0, 5.0)
    temp = st.sidebar.slider("Temp. Articulație (°C)", 20.0, 90.0, 45.0)
    vibra = st.sidebar.slider("Vibrații (m/s²)", 0.1, 6.0, 0.5)
    curent = st.sidebar.slider("Curent Motor (A)", 2.0, 15.0, 6.5)
    ore = st.sidebar.slider("Ore Funcționare", 0, 1000, 200)
    reteta = st.sidebar.selectbox("Rețetă", [0, 1, 2])
    
    data = {
        "setare_viteza_operare": viteza,
        "setare_sarcina_utila": sarcina,
        "senz_temperatura_articulatie_3": temp,
        "senz_vibratii_efector_final": vibra,
        "senz_curent_consumat_motor_1": curent,
        "ore_functionare_de_la_revizie": ore,
        "reteta_productie_activa": reteta
    }
    return pd.DataFrame([data])

input_df = user_input()

st.subheader("1. Date Senzori (Simulare)")
st.dataframe(input_df)

st.markdown("---")
if st.button("Rulează Prognoza AI", type="primary"):
    if scaler and model:
        input_processed = scaler.transform(input_df)
        
        pred = model.predict(input_processed)
        
        val_sarcina = input_df["setare_sarcina_utila"].values[0]
        val_viteza = input_df["setare_viteza_operare"].values[0] 
        val_ore = input_df["ore_functionare_de_la_revizie"].values[0] 
        factor_sarcina = (val_sarcina / 10.0) 
        factor_viteza = (val_viteza / 100.0)
        factor_uzura = (val_ore / 1000.0)

        bias_risc = (factor_sarcina * 0.5) + (factor_uzura * 0.3) + (factor_viteza * 0.1)
        
        raw_prob_mec = pred[0][0] + bias_risc
        raw_prob_el = pred[0][1] + bias_risc
        
        penalizare_calitate = (factor_sarcina * 40) + (factor_viteza * 20)
        raw_calitate = (pred[0][2] * 100) - penalizare_calitate
        
        prob_mec = np.clip(raw_prob_mec, 0.0, 1.0)
        prob_el = np.clip(raw_prob_el, 0.0, 1.0)
        
        calitate = np.clip(raw_calitate, 0.0, 100.0)
        
        timp_raw = 12.0 + (pred[0][3] * 5) + (factor_uzura * 2.0)
        timp_ciclu = max(0.1, timp_raw)

        st.subheader("2. Rezultate Analiză")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Risc Mecanic", f"{prob_mec:.1%}", help="Probabilitate defectare rulmenti/brate")
        col2.metric("Risc Electric", f"{prob_el:.1%}", help="Probabilitate scurtcircuit/supraincalzire motor")
        col3.metric("Calitate", f"{calitate:.1f}/100", help="Scor calitate piesa produsa")
        col4.metric("Timp Ciclu", f"{timp_ciclu:.2f} s", help="Durata estimata a operatiunii")
        
        st.markdown("### Status Sistem:")
        if prob_mec > 0.5 or prob_el > 0.5:
            st.error("ALERTA: Risc mare de defectiune! Verificati stocurile de piese.")
        elif calitate < 80:
            st.warning("ATENTIE: Calitatea scade sub nivelul optim.")
        else:
            st.success("NOMINAL: Parametrii sunt in limite normale.")
            
    else:
        st.error("Lipsesc fisierele modelului.")