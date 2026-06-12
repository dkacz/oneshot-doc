from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
ASSETS_DIR = REPO_ROOT / "assets"
sys.path.insert(0, str(ASSETS_DIR))

from palette import get_theme, save, setup_fonts
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the synthetic sample figure.")
    parser.add_argument("--theme", default="think-tank")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    theme = get_theme(args.theme)
    setup_fonts(theme=args.theme)

    labels = ["Baseline", "Target", "Stretch"]
    values = [42, 57, 63]

    fig, ax = plt.subplots(figsize=(5.8, 2.8))
    bars = ax.bar(labels, values, color=[theme["gray"], theme["primary"], theme["accent"]], width=0.56)
    ax.set_ylim(0, 72)
    ax.set_ylabel("percent")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 2,
            f"{value}%",
            ha="center",
            va="bottom",
            color=theme["gray"],
            fontsize=10.5,
        )
    ax.set_title("Readiness path", color=theme["primary"], fontweight="bold", pad=10)
    fig.tight_layout()
    save(fig, Path(__file__).with_suffix(".png"))


if __name__ == "__main__":
    main()
