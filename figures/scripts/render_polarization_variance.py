#!/usr/bin/env python3
"""Generate polarization-variance figure panels using the governing moments formula.

Each panel plots a normal density with E[X]=mu and Var(X)=sigma^2,
then reports B(X)=E[X^2] and Var(X)=E[X^2]-[E(X)]^2.
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "text.latex.preamble": r"\usepackage{amsmath} \usepackage{amssymb}",
})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=".", help="Directory to write figure PNGs")
    parser.add_argument(
        "--x-range",
        type=float,
        default=8.0,
        help="Half-width of x domain for plotting",
    )
    return parser.parse_args()


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    z = (x - mu) / sigma
    return np.exp(-0.5 * z**2) / (sigma * np.sqrt(2.0 * np.pi))


def render_one(path: Path, mu: float, sigma: float, x_max: float) -> None:
    x = np.linspace(-x_max, x_max, 4000)
    y = normal_pdf(x, mu, sigma)

    m1 = mu
    b = m1**2 + sigma**2
    var = b - m1**2

    fig, ax = plt.subplots(figsize=(4.6, 3.0), dpi=360)
    ax.plot(x, y, linewidth=2.1, color="#1f78b4")

    # Style and geometry
    ax.set_xlim(-x_max, x_max)
    ax.set_ylim(0.0, 0.95 / sigma)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f_{X\mid s_A}(x)$")
    ax.set_title(r"Ambitious-signal type dispersion")
    ax.grid(alpha=0.22, linewidth=0.6)

    # formula annotation
    ax.text(
        0.5,
        0.95,
        rf"$\mu={m1:.1f} \quad \mathrm{{Var}}(\theta \mid s_A)={var:.2f} \quad \mathbb{{E}}[\theta^2 \mid s_A]={b:.2f}$",
        transform=ax.transAxes,
        va="top",
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#cccccc"),
    )

    # Keep key formula visible and aligned with your section text
    ax.text(
        0.5,
        0.06,
        r"$\mathrm{Var}(\theta \mid s_A)=\mathbb{E}[\theta^2 \mid s_A]-(\mathbb{E}[\theta \mid s_A])^2$",
        transform=ax.transAxes,
        va="bottom",
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#cccccc"),
    )

    ax.tick_params(labelsize=10)
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=2)

    # optional 1-sigma support visualization
    ax.axvline(m1 - sigma, color="#d95f02", linestyle="--", alpha=0.7, linewidth=1.0)
    ax.axvline(m1 + sigma, color="#d95f02", linestyle="--", alpha=0.7, linewidth=1.0)

    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    specs = [
        ("model-variance-01-v1p21.png", 1.1),
        ("model-variance-02-v4p84.png", 2.2),
        ("model-variance-03-v10p24.png", 3.2),
    ]

    for fname, sigma in specs:
        path = out_dir / fname
        render_one(path=path, mu=0.0, sigma=sigma, x_max=args.x_range)


if __name__ == "__main__":
    main()
