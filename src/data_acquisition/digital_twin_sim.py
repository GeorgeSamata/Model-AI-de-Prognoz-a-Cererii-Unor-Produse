import pandas as pd
import numpy as np
import random

n_samples = 20000
data = []

print("Se generează baza de date simulată...")

current_wear = 0 

for i in range(n_samples):
    
    ore_funct = (i % 1000) + random.uniform(0, 5)
    
    if ore_funct < 20:
        current_wear = 0
        
    viteza = random.uniform(50, 100)
    sarcina = random.uniform(0.5, 10.0) 
    reteta = random.choice([0, 1, 2]) 
    
    wear_factor = (ore_funct / 1000) * 0.4 + (sarcina / 20) * 0.1
    current_wear = current_wear * 0.995 + wear_factor * 0.005
    
    temp = 40 + (viteza/10) + (current_wear * 25) + np.random.normal(0, 1.5)
    
    vibratii = 0.5 + (current_wear * 1.5) + (viteza/200) + np.random.normal(0, 0.1)
    if current_wear > 0.85:
        vibratii += random.uniform(1.0, 3.5)
        
    curent = 2.0 + (sarcina * 0.9) + (current_wear * 2.0) + np.random.normal(0, 0.2)
    
    
    prob_mec = 0.05
    if vibratii > 2.5:
        prob_mec = 0.9 + random.uniform(-0.05, 0.05)
    elif vibratii > 1.5:
        prob_mec = 0.4 + random.uniform(-0.1, 0.1)
        
    prob_el = 0.02
    if curent > 13.0:
        prob_el = 0.85 + random.uniform(-0.05, 0.05)
        
    calitate = 100 - (vibratii * 12) - np.random.normal(0, 2)
    calitate = max(0, min(100, calitate))
    
    timp_ciclu = 12.5 + (current_wear * 3) + np.random.normal(0, 0.1)

    row = {
        "setare_viteza_operare": round(viteza, 2),
        "setare_sarcina_utila": round(sarcina, 2),
        "senz_temperatura_articulatie_3": round(temp, 2),
        "senz_vibratii_efector_final": round(vibratii, 4),
        "senz_curent_consumat_motor_1": round(curent, 2),
        "ore_functionare_de_la_revizie": round(ore_funct, 1),
        "reteta_productie_activa": reteta,
        "prob_cerere_piesa_mecanica_24h": round(min(1.0, prob_mec), 4),
        "prob_cerere_piesa_electrica_24h": round(min(1.0, prob_el), 4),
        "estimare_calitate_produs_finit": round(calitate, 2),
        "estimare_timp_ciclu_secunde": round(timp_ciclu, 2)
    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv("baza_de_date_robot.csv", index=False)
print("Gata! Fisierul 'baza_de_date_robot.csv' a fost creat.")