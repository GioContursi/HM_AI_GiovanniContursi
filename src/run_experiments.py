from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from task1_problem.nqueens import NQueens
from task2_A.astar import a_star
from task2_A.heuristics import h0, h_rimanenti
from task2_B_CSP.nqueens_z3 import risolvi_nqueens_z3


def main() -> None:
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "results.csv"

    ns = [8, 10, 12, 14]

    campi = ["metodo", "n", "trovata_soluzione", "tempo_sec", "nodi_espansi", "nodi_generati", "max_frontiera"]

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        f.flush()

        for n in ns:
            print(f"\n=== n={n} ===")
            problema = NQueens(n)

            configurazioni: List[Tuple[str, Callable, str]] = []
            if n <= 10:
                configurazioni.append(("A*_h0_g_alto", h0, "g_alto"))
                configurazioni.append(("A*_h0_g_basso", h0, "g_basso"))
            configurazioni.append(("A*_h_rem_g_alto", h_rimanenti(n), "g_alto"))
            if n <= 10:
                configurazioni.append(("A*_h_rem_g_basso", h_rimanenti(n), "g_basso"))

            for nome, h, tb in configurazioni:
                print(f"  -> {nome}")
                sol, stats = a_star(problema, euristica=h, tie_break=tb)
                riga: Dict[str, object] = {
                    "metodo": nome,
                    "n": n,
                    "trovata_soluzione": sol is not None,
                    "tempo_sec": stats.tempo_sec,
                    "nodi_espansi": stats.nodi_espansi,
                    "nodi_generati": stats.nodi_generati,
                    "max_frontiera": stats.max_frontiera,
                }
                w.writerow(riga)
                f.flush()

            print("  -> CSP_Z3")
            sol_csp, stats_csp = risolvi_nqueens_z3(n)
            w.writerow(
                {
                    "metodo": "CSP_Z3",
                    "n": n,
                    "trovata_soluzione": sol_csp is not None,
                    "tempo_sec": stats_csp.tempo_sec,
                    "nodi_espansi": "",
                    "nodi_generati": "",
                    "max_frontiera": "",
                }
            )
            f.flush()

    print(f"\nSalvato: {out_csv}")


if __name__ == "__main__":
    main()
