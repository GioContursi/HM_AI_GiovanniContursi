# HM_AI_GiovanniContursi
Repository dell'homework svolto per il corso di Artificial Intelligence. Contursi Giovanni matricola: 2257249
-Descrizione:
Questo progetto implementa la soluzione dell’homework di Intelligenza Artificiale scegliendo come problema scalabile 
"n-Queens" (parametro `n`).

Sono state sviluppate le seguenti parti richieste dalla traccia:
- Task 1: modellazione e implementazione del problema scelto.
- Task 2.1 : risoluzione con "*A\", includendo gestione di euristiche e la variante richiesta (duplicate elimination / no reopening).
- Task 2.2: risoluzione con una seconda tecnica basata su **CSP**, utilizzando **Z3**.
- Task 3: valutazione sperimentale al variare di `n`, con salvataggio delle metriche in un file CSV e generazione di grafici.

## Dipendenze e installazione

Dipendenze Python (inserite in: `requirements.txt`):
- `z3-solver`
- `pandas`
- `matplotlib`

Da powershell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

