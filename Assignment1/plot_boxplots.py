import csv
from pathlib import Path
import matplotlib.pyplot as plt

IN_DIR = Path("benchmarks")

def read_ms(path):
    xs = []
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            xs.append(float(row["latency_ms"]))
    return xs

def main():
    q1 = read_ms(IN_DIR / "q1_category_year.csv")
    q2 = read_ms(IN_DIR / "q2_motivation.csv")
    q3 = read_ms(IN_DIR / "q3_name.csv")

    plt.figure(figsize=(8, 5))

    # ⚙️ Horizontal boxplot, matching the orientation of the example
    plt.boxplot(
        [q1, q2, q3],
        vert=False,                             # horizontal layout
        tick_labels=["Query 1", "Query 2", "Query 3"],
        patch_artist=True,                      # filled boxes
        boxprops=dict(facecolor="lightgreen", color="darkgreen"),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker='o', color='darkgreen', alpha=0.6)
    )

    plt.xlabel("End-to-End Delay (ms)")
    plt.ylabel("Queries")
    plt.title("gRPC End-to-End Latency (100 runs each) — Horizontal Box Plot")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    plt.savefig(IN_DIR / "latency_boxplots_horizontal.png", dpi=150)
    print(f"Saved: {(IN_DIR / 'latency_boxplots_horizontal.png').resolve()}")

if __name__ == "__main__":
    main()
