Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

Disciplina: Rețele Neuronale
Instituție: POLITEHNICA București – FIIR
Student: Șamata George Cristian
Data: 03.12.2025

Scopul Etapei 4

Livrarea unui SCHELET COMPLET și FUNCȚIONAL al întregului Sistem cu Inteligență Artificială (SIA). În acest stadiu modelul RN este definit și compilat (arhitectură MLP), iar pipeline-ul de date funcționează cap-coadă.

1. Tabelul Nevoie Reală → Soluție SIA → Modul Software

Nevoie reală concretă
Cum o rezolvă SIA-ul vostru
Modul software responsabil
Reducerea opririlor neplanificate ale roboților industriali pe linia de asamblare
Predicția probabilității de defectare mecanică/electrică cu 24h înainte (Output > 80%)
src/neural_network (Model MLP) + src/app (Alertare UI)
Optimizarea stocului de piese de schimb (rulmenți, motoare)
Prognoza cererii specifice de piese: sistemul indică exact ce tip de componentă se va defecta
src/data_acquisition (Simulare) + src/app (Dashboard)
Asigurarea calității constante a produsului finit (ex: sudură)
Corelarea vibrațiilor și uzurii cu un scor de calitate estimat în timp real
src/app/dashboard.py (Monitorizare continuă)

2. Contribuția Originală la Setul de Date

Total observații finale: 20,000
Observații originale: 20,000 (100%)

Tipul contribuției:
[X] Date generate prin simulare fizică (Digital Twin)

Descriere detaliată:
Am dezvoltat un simulator software (digital_twin_sim.py) care modelează fizica degradării unui braț robotic industrial pe parcursul a 6 luni de funcționare continuă. Simulatorul generează date sintetice pentru 7 senzori critici (viteză, sarcină, temperatură, vibrații, curent, ore funcționare, rețetă).
Contribuția constă în implementarea unor corelații realiste între parametrii de operare și uzură (ex: vibrațiile cresc exponențial odată cu uzura mecanică; temperatura motorului crește liniar cu viteza și sarcina). De asemenea, am introdus scenarii de defect ("failure modes") specifice pentru componente mecanice și electrice.
Locația codului: src/data_acquisition/digital_twin_sim.py
Locația datelor: data/raw/simulation_output_v1.csv

3. Diagrama State Machine a Sistemului

Justificarea State Machine-ului ales:
Am ales o arhitectură de Monitorizare Continuă cu Feedback (Continuous Monitoring). Aceasta este standardul în sistemele SCADA și Industry 4.0, unde sistemul citește senzorii în buclă infinită, procesează datele și alertează operatorul doar când sunt depășite pragurile de siguranță.

Stările Principale:
IDLE: Sistemul așteaptă input de la utilizator sau conectarea la fluxul de date.
ACQUIRE_DATA: Citirea valorilor simulate de la cei 7 senzori (prin sliderele din UI).
PREPROCESS: Normalizarea datelor (MinMax Scaler) pentru a aduce valorile fizice (ex: 90°C) în intervalul [0,1].
INFERENCE: Modelul RN (MLP Regressor) calculează cele 4 predicții (Risc Mecanic, Risc Electric, Calitate, Timp).
CHECK_THRESHOLDS: Verificarea logică a rezultatelor (ex: Dacă Risc > 50% → STARE DE ALERTĂ).
DISPLAY: Afișarea rezultatelor și a mesajelor de avertizare în Dashboard.
Flux:
IDLE → ACQUIRE → PREPROCESS → INFERENCE → CHECK → DISPLAY → IDLE (Loop)
(Diagrama vizuală este salvată în folderul docs/)

4. Structura Modulelor

Modul
Cale Fișier
Rol

1. Data Logging / Acquisition
src/data_acquisition/digital_twin_sim.py
Generează datele brute CSV simulând fizica robotului. Rulează fără erori și produce 20k samples.

2. Neural Network Module
src/neural_network/model.py
Definește și salvează arhitectura MLP (Scikit-Learn). Modelul este salvat ca untrained_model.pkl.

3. Web Service / UI
src/app/dashboard.py
Interfața Streamlit. Permite simularea senzorilor, apelează modelul și afișează riscurile calculate.
Checklist Final – Etapa 4
[x] Tabelul Nevoie → Soluție completat
[x] Declarație contribuție 100% date originale (Digital Twin)
[x] Cod generare date funcțional (digital_twin_sim.py)
[x] Repository structurat corect (data, src, docs, models)
[x] Modul 1 (Acquisition): CSV generat cu succes
[x] Modul 2 (RN): Arhitectură definită, model salvat .pkl
[x] Modul 3 (UI): Dashboard funcțional, calculează și afișează prognoza