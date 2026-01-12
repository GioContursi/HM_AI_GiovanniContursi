from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def _etichetta_metodo(m: str) -> str:
    mapping = {
        "A*_h0_g_alto": "A* (h=0)",
        "A*_h0_g_basso": "A* (h=0)",
        "A*_h_rem_g_alto": "A* (euristica 1)",
        "A*_h_rem_g_basso": "A* (euristica 1, variante)",
        "CSP_Z3": "CSP (Z3)",
    }
    return mapping.get(m, m)


def main() -> None:
    csv_path = Path("outputs/results.csv")
    df = pd.read_csv(csv_path)

    df["tempo_sec"] = pd.to_numeric(df["tempo_sec"], errors="coerce")
    df["nodi_espansi"] = pd.to_numeric(df["nodi_espansi"], errors="coerce")
    df["metodo_label"] = df["metodo"].astype(str).map(_etichetta_metodo)

    out_dir = Path("outputs/plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Tempo vs n
    plt.figure()
    for label, g in df.groupby("metodo_label"):
        gg = g.sort_values("n")
        plt.plot(gg["n"], gg["tempo_sec"], marker="o", label=label)
    plt.xlabel("n")
    plt.ylabel("tempo (s)")
    plt.title("Tempo di esecuzione al variare di n")
    plt.legend()
    plt.savefig(out_dir / "tempo_vs_n.png", bbox_inches="tight")
    plt.close()

    # Nodi espansi vs n (solo A*)
    df_a = df[df["metodo"].astype(str).str.startswith("A*")].copy()
    plt.figure()
    for label, g in df_a.groupby("metodo_label"):
        gg = g.sort_values("n")
        plt.plot(gg["n"], gg["nodi_espansi"], marker="o", label=label)
    plt.xlabel("n")
    plt.ylabel("nodi espansi")
    plt.title("Nodi espansi di A* al variare di n")
    plt.legend()
    plt.savefig(out_dir / "nodi_espansi_vs_n.png", bbox_inches="tight")
    plt.close()

    print(f"Creati grafici in: {out_dir}")


if __name__ == "__main__":
    main()
