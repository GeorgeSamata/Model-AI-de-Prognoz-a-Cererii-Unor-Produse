
## 2. Descrierea Setului de Date

### 2.1 Sursa datelor

* **Origine:** Date sintetice generate folosind un model de simulare  al brațului robotic industrial, creat pentru a replica scenarii de uzură accelerată și defecțiuni controlate.
* **Modul de achiziție:**  Simulare /  Generare programatică (Nu s-au folosit senzori reali fizici în această etapă).
* **Perioada / condițiile colectării:** Datele simulează o funcționare continuă echivalentă cu 6 luni de producție, incluzând cicluri normale, suprasolicitări și degradarea progresivă a componentelor până la defectare.

### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:** 20,000 (linii/eșantioane temporale).
* **Număr de caracteristici (features):** 11 coloane (7 variabile de intrare + 4 variabile țintă/ieșire).
* **Tipuri de date:**  Numerice (majoritare, float) /  Categoriale (rețeta de producție).
* **Format fișiere:**  CSV (Comma Separated Values).

### 2.3 Descrierea fiecărei caracteristici

Tabelul de mai jos detaliază variabilele monitorizate (intrările) și valorile pe care modelul învață să le prezică (ieșirile).

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
| :--- | :--- | :--- | :--- | :--- |
| **INTRĂRI (INPUTS)** | | | | |
| `setare_viteza_operare` | Numeric | % | Viteza programată a robotului raportată la maximul nominal. | 50.0 – 100.0 |
| `setare_sarcina_utila` | Numeric | kg | Greutatea obiectului manipulat în ciclul curent. | 0.5 – 10.0 |
| `senz_temperatura_articulatie_3`| Numeric | °C | Temperatura măsurată la nivelul articulației "cotului" (cea mai solicitată). | 20.0 – 85.0 |
| `senz_vibratii_efector_final` | Numeric | m/s² | Nivelul de vibrație măsurat prin accelerometru la capul robotului. | 0.1 – 5.5 |
| `senz_curent_consumat_motor_1` | Numeric | Amperi | Intensitatea curentului absorbit de motorul principal (baza). | 2.0 – 15.0 |
| `ore_functionare_de_la_revizie`| Numeric | Ore | Timpul scurs de la ultima intervenție de mentenanță preventivă. | 0 – 1,000 |
| `reteta_productie_activa` | Categorial| ID | Codul numeric al tipului de operațiune executată (ex: sudură, manipulare). | {0, 1, 2} |
| **IEȘIRI (TARGETS)** | | | | |
| `prob_cerere_piesa_mecanica_24h` | Numeric | Prob. (0-1)| Probabilitatea estimată de defectare a unei componente mecanice în următoarele 24h. | 0.00 – 1.00 |
| `prob_cerere_piesa_electrica_24h`| Numeric | Prob. (0-1)| Probabilitatea estimată de defectare a unei componente electrice în următoarele 24h. | 0.00 – 1.00 |
| `estimare_calitate_produs_finit` | Numeric | Scor | Indicator sintetic al calității execuției (ex: precizia pe traiectorie). | 10.0 – 100.0 |
| `estimare_timp_ciclu_secunde` | Numeric | Secunde | Durata efectivă a ciclului curent (influențată de uzură/vibrații). | 12.5 – 18.0 |

## 3. Analiza Exploratorie a Datelor (EDA) – Sintetic

Deoarece setul de date a fost generat prin simulare, analiza exploratorie a vizat validarea comportamentului fizic al modelului simulat și identificarea distribuțiilor care vor influența antrenarea rețelei neuronale.

### 3.1 Statistici descriptive aplicate

S-a realizat o analiză statistică pe cele 20.000 de observații pentru a înțelege tendința centrală și dispersia datelor.

* **Tabel sintetic al distribuțiilor (Intrări Principale):**

| Caracteristică | Medie (Mean) | Mediană | Deviație Std | Min | Max | Observații |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `senz_temperatura_articulatie_3` | 42.5 °C | 40.1 °C | ±12.4 | 20.0 | 85.0 | Distribuție normală, cu o "coadă" lungă spre dreapta (cazurile de supraîncălzire). |
| `senz_vibratii_efector_final` | 0.8 m/s² | 0.5 m/s² | ±0.9 | 0.1 | 5.5 | Majoritatea valorilor sunt mici (funcționare normală). Valorile > 3.0 sunt rare (anomalii). |
| `senz_curent_consumat_motor_1` | 6.2 A | 5.8 A | ±2.1 | 2.0 | 15.0 | Variază liniar cu sarcina utilă, dar prezintă spike-uri în scenariile de defect electric. |
| `ore_functionare_de_la_revizie` | 480 h | 500 h | ±280 | 0 | 1000 | Distribuție uniformă (simularea acoperă întregul ciclu de viață între revizii). |

* **Distribuții și Histograme:**
    Histogramele indică faptul că variabilele senzoriale (`vibratii`, `temperatura`) nu urmează o distribuție perfect Gaussiană, ci sunt distribuții *bimodale*: un "vârf" mare în zona valorilor mici (funcționare normală) și un "vârf" mic și dispersat în zona valorilor mari (stări de defect).
* **Identificarea Outlierilor:**
    Folosind metoda IQR (Interquartile Range), s-au identificat numeroși "outlieri" matematici la senzorul de vibrații (valori > 1.5 * IQR). În contextul mentenanței predictive, acești "outlieri" nu sunt erori, ci reprezintă **exact semnalele critice de defecțiune** pe care rețeaua neuronală trebuie să le învețe.

### 3.2 Analiza calității datelor

Fiind un dataset sintetic generat controlat, calitatea tehnică este superioară datelor brute reale, însă analiza a relevat structuri interne importante:

* **Detectarea valorilor lipsă:** 0% valori lipsă (NaN) pe toate coloanele. Simularea a fost continuă, fără pierderi de pachete de date.
* **Matricea de Corelație (Heatmap):**
    
    S-a observat o corelație puternică pozitivă (0.85) între `senz_vibratii_efector_final` și variabila țintă `prob_cerere_piesa_mecanica_24h`.
    De asemenea, există o corelație inversă (negativă) puternică între `senz_vibratii_efector_final` și `estimare_calitate_produs_finit` (vibrațiile mari scad calitatea).
* **Redundanță:** Variabila `setare_sarcina_utila` și `senz_curent_consumat_motor_1` sunt parțial corelate (sarcina mai mare cere curent mai mare), dar curentul conține informație suplimentară despre starea de sănătate a motorului (frecări interne), deci ambele caracteristici sunt păstrate.

### 3.3 Probleme identificate

În urma analizei EDA, au fost identificate următoarele provocări pentru etapa de modelare:

* **Dezechilibru Major de Clase (Class Imbalance):** Aceasta este cea mai mare problemă. Doar aproximativ 15% din date reprezintă stări de "alertă" sau "defect", restul de 85% fiind funcționare normală.
    * Impact: Rețeaua ar putea fi tentată să prezică mereu "Totul e OK" și să aibă o acuratețe de 85%, dar să fie inutilă. Va fi necesară utilizarea unor tehnici de ponderare a erorii (class weighting) în antrenare.
* **Scări de Valori Diferite (Scaling):** Variabilele au magnitudini foarte diferite (Procente 0-100 vs. Vibrații 0-5 vs. Ore 0-1000).
    * Impact: Rețeaua neuronală va converge greu. Este obligatorie normalizarea datelor (ex: Min-Max Scaling) în intervalul [0, 1] înainte de antrenare.
* **Dependență Temporală:** Datele nu sunt independente (I.I.D.), ci secvențiale (starea la momentul *t* depinde de *t-1*).
    * Impact: O rețea simplă feed-forward (MLP) s-ar putea să nu fie suficientă; EDA sugerează necesitatea unei arhitecturi recurente (RNN/LSTM) sau includerea unui "fereastre glisante" (sliding window) de intrări.


## 4. Preprocesarea Datelor

Etapa de preprocesare este critică pentru performanța rețelei neuronale, transformând datele brute simulate într-un format numeric optimizat pentru antrenare.

### 4.1 Curățarea datelor

Deoarece datele provin dintr-o simulare controlată (Digital Twin), setul de date este tehnic "curat", dar au fost aplicați pași de validare:

* **Eliminarea duplicatelor:** S-a verificat unicitatea timestamp-urilor. Nu au fost identificate duplicate (0 înregistrări eliminate).
* **Tratarea valorilor lipsă:** Nu există valori lipsă (NaN) în dataset-ul simulat. Nu a fost necesară imputarea (umplerea) datelor.
* **Tratarea outlierilor:**
    * *Abordare Specifică PdM (Predictive Maintenance):* Valorile extreme ("outlieri" statistici) identificate în faza de EDA la senzorii de **vibrații** și **curent** au fost **păstrate intenționat**.
    * *Motivație:* În acest context, un vârf de vibrație nu este o eroare de măsurare, ci semnătura unei defecțiuni iminente. Eliminarea lor ar fi șters exact informația pe care modelul trebuie să o învețe.

### 4.2 Transformarea caracteristicilor

* **Normalizare (Scaling):**
    * S-a utilizat metoda **Min-Max Scaling** pentru a aduce toate variabilele numerice continue în intervalul `[0, 1]`.
    * Acest pas este esențial deoarece intrările au scări foarte diferite (ex: Temperatura ≈ 80°C vs. Vibrații ≈ 0.5 m/s²), iar rețelele neuronale converg mult mai greu fără normalizare.
    * *Excepție:* Variabilele țintă (probabilitățile de ieșire) sunt deja în intervalul 0-1.
* **Encoding pentru variabile categoriale:**
    * Variabila `reteta_productie_activa` (valori 0, 1, 2) a fost transformată folosind **One-Hot Encoding**.
    * *Rezultat:* O singură coloană a devenit 3 coloane binare (ex: `reteta_0`, `reteta_1`, `reteta_2`). Aceasta previne modelul să interpreteze eronat că rețeta "2" este matematic mai mare decât rețeta "1".
* **Ajustarea dezechilibrului de clasă:**
    * Deși datele sunt dezechilibrate (mult mai multe date "normale" decât "defect"), nu s-a folosit *Resampling* (ștergerea/duplicarea datelor) în această etapă pentru a nu distruge continuitatea temporală.
    * *Soluție:* Gestionarea dezechilibrului se va face în etapa de antrenare prin parametrul `class_weight` în funcția de pierdere (Loss Function).

#   M o d e l - A I - d e - P r o g n o z - a - C e r e r i i - U n o r - P r o d u s e  
 