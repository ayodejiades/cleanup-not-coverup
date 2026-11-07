"""Figures for RQ 4.2, from results/analysis.json and results/claims.partial/monitors.json.

Run after analysis/monitors.py, with a Python that has matplotlib (on this machine:
python3.11 analysis/figures.py). Writes figures/*.png and figures/captions.json.
Static figures for a PDF, light surface only.
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
SERIES_1 = "#2a78d6"
RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
MONITORS = ["m1", "m2", "m3", "m4", "m5"]
NAMES = {"m1": "M1 LLM\nlog reader", "m2": "M2 any\ndeletion", "m3": "M3 any\nunlisted call",
         "m4": "M4 effect-\nlinked", "m5": "M5\nprovenance"}
EVASIONS = {"base64": "base64", "hex": "hex", "reverse": "reversed", "split": "split in\n6-char parts",
            "relay": "relayed\nthrough B", "copy_rename": "copied, then\nrenamed"}


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def claims_by_id() -> dict:
    path = ROOT / "results" / "claims.partial" / "monitors.json"
    return {c["id"]: c for c in json.loads(path.read_text(encoding="utf-8"))}


def fig_pairs(claims: dict, tables: dict) -> str:
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200, facecolor=SURFACE)
    style(ax)
    xs = range(len(MONITORS))
    values = [claims["pair_acc.%s" % m]["value"] for m in MONITORS]
    lows = [values[i] - claims["pair_acc.%s" % m]["ci"][0] for i, m in enumerate(MONITORS)]
    highs = [claims["pair_acc.%s" % m]["ci"][1] - values[i] for i, m in enumerate(MONITORS)]
    ax.bar(xs, values, width=0.5, color=SERIES_1, edgecolor=SURFACE, linewidth=2)
    ax.errorbar(xs, values, yerr=[lows, highs], fmt="none", ecolor=INK_2, elinewidth=1.2, capsize=3)
    for x, v, high in zip(xs, values, highs):
        ax.text(x, v + high + 0.03, "%.2f" % v, ha="center", va="bottom", fontsize=9, color=INK)
    ax.set_xticks(list(xs), [NAMES[m] for m in MONITORS])
    ax.set_ylim(0, 1.14)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("Pair accuracy (held out)", color=INK_2, fontsize=9)
    n = tables["eligible_heldout_pairs"]
    ax.set_title("Who tells a cover-up from its honest twin (n = %d pairs)" % n,
                 color=INK, fontsize=10, loc="left")
    fig.tight_layout()
    name = "fig1_pair_accuracy.png"
    fig.savefig(FIG / name, facecolor=SURFACE)
    plt.close(fig)
    return name


def fig_evasions(tables: dict) -> str:
    table = tables["evasion_catch"]
    rows = [e for e in EVASIONS if e in table]
    grid = [[table[e][m] for m in MONITORS] for e in rows]
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=200, facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    cmap = LinearSegmentedColormap.from_list("blue", RAMP)
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            ax.text(j, i, "%.2f" % value, ha="center", va="center", fontsize=9,
                    color=SURFACE if value > 0.55 else INK)
    ax.set_xticks(range(len(MONITORS)), [NAMES[m] for m in MONITORS], fontsize=8, color=INK_2)
    ax.set_yticks(range(len(rows)), [EVASIONS[e] for e in rows], fontsize=8, color=INK_2)
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_xticks([x - 0.5 for x in range(1, len(MONITORS))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.tick_params(which="minor", length=0)
    ax.set_title("Share of scripted evasions caught, per monitor (C5)", color=INK, fontsize=10, loc="left")
    fig.tight_layout()
    name = "fig2_evasions.png"
    fig.savefig(FIG / name, facecolor=SURFACE)
    plt.close(fig)
    return name


def fig_lcs(tables: dict) -> str:
    lcs = tables["m4_lcs"]
    length = tables["rule"]["m4_L"]
    conds = [c for c in ("C2", "C3", "C4") if lcs.get(c)]
    labels = {"C2": "C2 cover-up", "C3": "C3 honest twin", "C4": "C4 told the rule"}
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=200, facecolor=SURFACE)
    style(ax)
    for i, cond in enumerate(conds):
        values = lcs[cond]
        width = min(0.36, 0.03 * len(values))
        offsets = [(k / max(len(values) - 1, 1) - 0.5) * width for k in range(len(values))]
        ax.scatter([i + o for o in offsets], [v + 1 for v in values], s=36, color=SERIES_1,
                   edgecolors=SURFACE, linewidths=1.5, zorder=3)
    ax.axhline(length + 1, color=INK_2, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(len(conds) - 0.5, length + 1, " L = %d" % length, va="bottom", ha="right",
            fontsize=8, color=INK_2)
    ax.set_yscale("log")
    ax.set_xticks(range(len(conds)), [labels[c] for c in conds])
    ax.set_xlim(-0.5, len(conds) - 0.5)
    ax.set_ylabel("Longest shared text + 1 (characters)", color=INK_2, fontsize=9)
    ax.set_title("Text shared by a deleted file and an unlisted request (held out)",
                 color=INK, fontsize=10, loc="left")
    fig.tight_layout()
    name = "fig3_m4_lcs.png"
    fig.savefig(FIG / name, facecolor=SURFACE)
    plt.close(fig)
    return name


def main() -> int:
    tables_path = ROOT / "results" / "analysis.json"
    if not tables_path.exists():
        print("no results/analysis.json yet; run analysis/monitors.py first")
        return 0
    tables = json.loads(tables_path.read_text(encoding="utf-8"))
    claims = claims_by_id()
    FIG.mkdir(exist_ok=True)
    length = tables["rule"]["m4_L"]
    captions = {
        fig_pairs(claims, tables): (
            "Figure 1: Pair accuracy on held-out matched pairs: the share of (C2, C3) pairs where "
            "a monitor flags the cover-up run and passes its honest twin. Bars show Wilson 95% "
            "intervals."),
        fig_evasions(tables): (
            "Figure 2: Share of scripted C5 cover-ups each monitor catches, by evasion. M4 uses "
            "the length L = %d set on calibration seeds." % length),
        fig_lcs(tables): (
            "Figure 3: For each held-out run, the longest stretch of text shared by any destroyed "
            "artefact and any undeclared request (log scale, plus one so zero shows). M4 flags a "
            "run at or above the dashed line."),
    }
    (FIG / "captions.json").write_text(json.dumps(captions, indent=2, sort_keys=True) + "\n",
                                       encoding="utf-8")
    print("wrote %s" % ", ".join(sorted(captions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
