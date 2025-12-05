import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

RAW_DATA_PATH = "data/raw/simulation_output_v1.csv"
PROCESSED_PATH = "data/processed/"
TRAIN_PATH = "data/train/"
VAL_PATH = "data/validation/"
TEST_PATH = "data/test/"

FEATURE_COLS = [
    "setare_viteza_operare",
    "setare_sarcina_utila",
    "senz_temperatura_articulatie_3",
    "senz_vibratii_efector_final",
    "senz_curent_consumat_motor_1",
    "ore_functionare_de_la_revizie"
]
CAT_COL = ["reteta_productie_activa"]

TARGET_COLS = [
    "prob_cerere_piesa_mecanica_24h",
    "prob_cerere_piesa_electrica_24h",
    "estimare_calitate_produs_finit",
    "estimare_timp_ciclu_secunde"
]

def process_data():
    print("--- Start Preprocesare Date ---")
    
    if not os.path.exists(RAW_DATA_PATH):
        print(f"EROARE: Nu gasesc fisierul {RAW_DATA_PATH}. Ai rulat simulatorul?")
        return

    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Date incarcate: {df.shape}")
    
    X = df[FEATURE_COLS + CAT_COL]
    y = df[TARGET_COLS]
    

    total_len = len(df)
    train_end = int(total_len * 0.70)
    val_end = int(total_len * 0.85)
    
    X_train_raw = X.iloc[:train_end]
    y_train = y.iloc[:train_end]
    
    X_val_raw = X.iloc[train_end:val_end]
    y_val = y.iloc[train_end:val_end]
    
    X_test_raw = X.iloc[val_end:]
    y_test = y.iloc[val_end:]
    
    print(f"Split realizat: Train={len(X_train_raw)}, Val={len(X_val_raw)}, Test={len(X_test_raw)}")
    

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), FEATURE_COLS),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CAT_COL)
        ])
    
    print("Se antreneaza Scaler-ul pe datele de Train...")
    X_train_processed = preprocessor.fit_transform(X_train_raw)
    
    X_val_processed = preprocessor.transform(X_val_raw)
    X_test_processed = preprocessor.transform(X_test_raw)
    
    print("Salvare fisiere...")
    
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    os.makedirs(TRAIN_PATH, exist_ok=True)
    os.makedirs(VAL_PATH, exist_ok=True)
    os.makedirs(TEST_PATH, exist_ok=True)
    
    with open(os.path.join(PROCESSED_PATH, 'preprocessor.pkl'), 'wb') as f:
        pickle.dump(preprocessor, f)
        
    np.save(os.path.join(TRAIN_PATH, 'X_train.npy'), X_train_processed)
    np.save(os.path.join(TRAIN_PATH, 'y_train.npy'), y_train.to_numpy())
    
    np.save(os.path.join(VAL_PATH, 'X_val.npy'), X_val_processed)
    np.save(os.path.join(VAL_PATH, 'y_val.npy'), y_val.to_numpy())
    
    np.save(os.path.join(TEST_PATH, 'X_test.npy'), X_test_processed)
    np.save(os.path.join(TEST_PATH, 'y_test.npy'), y_test.to_numpy())
    
    print("--- Procesare Completa! Fisierele .npy au fost generate. ---")

if __name__ == "__main__":
    process_data()