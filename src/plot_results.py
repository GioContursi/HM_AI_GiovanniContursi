from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    csv_path = Path("outputs/results.csv")
    df = pd.read_csv(csv_path)

    df["tempo_sec"] = pd.to_numeric(df["tempo_sec"], errors="coerce")
    df["nodi_espansi"] = pd.to_numeric(df["nodi_espansi"], errors="coerce")

    out_dir = Path("outputs/plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.figure()
    for metodo, g in df.groupby("metodo"):
        plt.plot(g["n"], g["tempo_sec"], marker="o", label=metodo)
    plt.xlabel("n")
    plt.ylabel("tempo (sec)")
    plt.title("Tempo di esecuzione vs n")
    plt.legend()
    plt.savefig(out_dir / "tempo_vs_n.png", bbox_inches="tight")
    plt.close()


    df_a = df[df["metodo"].str.startswith("A*")].copy()
    plt.figure()
    for metodo, g in df_a.groupby("metodo"):
        plt.plot(g["n"], g["nodi_espansi"], marker="o", label=metodo)
    plt.xlabel("n")
    plt.ylabel("nodi espansi")
    plt.title("Nodi espansi vs n (A*)")
    plt.legend()
    plt.savefig(out_dir / "nodi_espansi_vs_n.png", bbox_inches="tight")
    plt.close()

    print(f"Creati grafici in: {out_dir}")


if __name__ == "__main__":
    main()