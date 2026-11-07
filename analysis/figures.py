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
RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
MONITORS = ["m1", "m2", "m3", "m4", "m5"]
NAMES = {"m1": "M1 LLM\nlog reader", "m2": "M2 any\ndeletion", "m3": "M3 any\nunlisted call",
         "m4": "M4 effect-\nlinked", "m5": "M5\nprovenance", "m1g": "M1g LLM on\ngateway record"}
EVASIONS = {"base64": "base64", "hex": "hex", "reverse": "reversed", "split": "split, 6 chars",
            "relay": "relayed via B", "copy_rename": "renamed copy"}


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


SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # categorical slots 1-3, fixed order
PAIR_SETS = [("", "Preregistered seeds"), ("ext.", "With the D1 extension"),
             ("expl.c4.", "C4 pairs (exploratory)")]


def bar_group(ax, claims: dict, series: list, key: str):
    """Grouped bars by monitor; series is [(claim prefix, label)] in fixed colour order.
    The exploratory M1g group is drawn after a dashed rule when its claims exist."""
    monitors = MONITORS + [m for m in ("m1g",)
                           if all((prefix + key % m) in claims for prefix, _ in series)]
    width = 0.8 / len(series)
    for k, (prefix, label) in enumerate(series):
        xs = [i + (k - (len(series) - 1) / 2) * width for i in range(len(monitors))]
        rows = [claims[prefix + key % m] for m in monitors]
        values = [r["value"] for r in rows]
        lows = [max(0.0, v - r["ci"][0]) for v, r in zip(values, rows)]
        highs = [max(0.0, r["ci"][1] - v) for v, r in zip(values, rows)]
        n = rows[0]["n"]
        ax.bar(xs, values, width=width * 0.92, color=SERIES[k], edgecolor=SURFACE, linewidth=1,
               label="%s (n = %d)" % (label, n))
        ax.errorbar(xs, values, yerr=[lows, highs], fmt="none", ecolor=INK_2, elinewidth=0.9,
                    capsize=2)
        for x, v, high in zip(xs, values, highs):
            ax.text(x, v + high + 0.02, "%.2f" % v, ha="center", va="bottom",
                    fontsize=6.5 if len(series) < 3 else 5.6, color=INK)
    ax.set_xticks(range(len(monitors)), [NAMES[m] for m in monitors])
    if len(monitors) > len(MONITORS):
        ax.axvline(len(MONITORS) - 0.5, color=INK_2, linewidth=0.8, linestyle=(0, (3, 3)))
        ax.text(len(MONITORS) - 0.42, 1.12, "exploratory", fontsize=7, color=INK_2,
                ha="left", va="center")
    ax.set_ylim(0, 1.2)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.tick_params(axis="x", labelsize=8)
    ax.legend(loc="lower left", fontsize=7.5, frameon=False, ncol=len(series),
              bbox_to_anchor=(0, 1.0), handlelength=1.2, columnspacing=1.2, labelcolor=INK_2,
              borderaxespad=0.2)


def fig_pairs(claims: dict) -> str:
    series = [(p, l) for p, l in PAIR_SETS if (p + "pair_acc.m1") in claims]
    claims = dict(claims)
    for prefix, part in (("", "prereg"), ("ext.", "ext"), ("expl.c4.", "c4")):
        if "expl.m1g.pair_acc.%s" % part in claims:
            claims[prefix + "pair_acc.m1g"] = claims["expl.m1g.pair_acc.%s" % part]
    fig, ax = plt.subplots(figsize=(6.4, 2.3), dpi=200, facecolor=SURFACE)
    style(ax)
    bar_group(ax, claims, series, "pair_acc.%s")
    ax.set_ylabel("Pair accuracy (held out)", color=INK_2, fontsize=9)
    ax.set_title("Flags the cover-up and passes its honest twin", color=INK, fontsize=10,
                 loc="left", pad=20)
    fig.tight_layout()
    name = "fig1_pair_accuracy.png"
    fig.savefig(FIG / name, facecolor=SURFACE)
    plt.close(fig)
    return name


def fig_reacts(claims: dict) -> str:
    prefix = "ext." if "ext.flag.C3.m1" in claims else ""
    view = {"c1.flag.%s" % m: claims[prefix + "flag.C1.%s" % m] for m in MONITORS}
    view.update({"c3.flag.%s" % m: claims[prefix + "flag.C3.%s" % m] for m in MONITORS})
    for cond in ("C1", "C3"):
        if "expl.m1g.flag.%s" % cond in claims:
            view["%s.flag.m1g" % cond.lower()] = claims["expl.m1g.flag.%s" % cond]
    fig, ax = plt.subplots(figsize=(6.4, 2.2), dpi=200, facecolor=SURFACE)
    style(ax)
    bar_group(ax, view, [("c1.", "C1 leak, no cleanup"), ("c3.", "C3 cleanup, no leak")],
              "flag.%s")
    ax.set_ylabel("Share of held-out runs flagged", color=INK_2, fontsize=9)
    ax.set_title("What each monitor reacts to", color=INK, fontsize=10, loc="left", pad=20)
    fig.tight_layout()
    name = "fig2_flag_rates.png"
    fig.savefig(FIG / name, facecolor=SURFACE)
    plt.close(fig)
    return name


def fig_evasions(tables: dict) -> str:
    table = tables["evasion_catch"]
    rows = [e for e in EVASIONS if e in table]
    grid = [[table[e][m] for m in MONITORS] for e in rows]
    fig, ax = plt.subplots(figsize=(6.4, 2.15), dpi=200, facecolor=SURFACE)
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
    name = "figS2_evasions.png"
    fig.savefig(FIG / name, facecolor=SURFACE)
    plt.close(fig)
    return name


def fig_lcs(tables: dict) -> str:
    lcs = tables["m4_lcs"]
    length = tables["rule"]["m4_L"]
    groups = [("C2", "cover_up", "C2\ncover-ups"), ("C2", "other", "C2, canary\nnot sent"),
              ("C3", "other", "C3\nhonest twins"), ("C4", "cover_up", "C4\ncover-ups"),
              ("C4", "other", "C4, canary\nnot sent")]
    groups = [g for g in groups if lcs.get(g[0], {}).get(g[1])]
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200, facecolor=SURFACE)
    style(ax)
    for i, (cond, kind, _) in enumerate(groups):
        values = lcs[cond][kind]
        # deterministic spread (golden-ratio sequence) so overlapping runs stay visible
        xs = [i + (((k * 0.6180339887) % 1.0) - 0.5) * 0.5 for k in range(len(values))]
        ax.scatter(xs, [v + 1 for v in values], s=14, color=SERIES[0], alpha=0.55,
                   edgecolors="none", zorder=3)
        ax.text(i, 1.0 * 0.62, "n = %d" % len(values), ha="center", va="top", fontsize=7.5,
                color=INK_2)
    ax.axhline(length + 1, color=INK_2, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(len(groups) - 0.55, (length + 1) * 1.08, "L = %d" % length, va="bottom", ha="right",
            fontsize=8, color=INK_2)
    ax.set_yscale("log")
    ax.set_ylim(0.45, 400)
    ax.set_xticks(range(len(groups)), [g[2] for g in groups], fontsize=8)
    ax.set_xlim(-0.5, len(groups) - 0.5)
    ax.set_ylabel("Longest shared text + 1 (characters)", color=INK_2, fontsize=9)
    ax.set_title("Text shared by a deleted file and an unlisted request (held out)",
                 color=INK, fontsize=10, loc="left")
    fig.tight_layout()
    name = "figS1_m4_lcs.png"
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
    n_c1 = claims[("ext." if "ext.flag.C3.m1" in claims else "") + "flag.C1.m1"]["n"]
    n_c3 = claims[("ext." if "ext.flag.C3.m1" in claims else "") + "flag.C3.m1"]["n"]
    for old in FIG.glob("fig*.png"):
        old.unlink()
    captions = {
        fig_pairs(claims): (
            "Figure 1: Pair accuracy (the share of held-out pairs in which a monitor flags the "
            "cover-up and passes its honest twin) on the preregistered seeds, with D1, and on "
            "exploratory C4 pairs. Error bars are Wilson 95% intervals. M1g, right of the dashed "
            "line, is the exploratory monitor of Section 4.5 at its calibrated threshold."),
        fig_reacts(claims): (
            "Figure 2: Share of held-out runs each monitor flags, for open leaks with no cleanup "
            "(C1, %d runs) and honest cleanup with no leak (C3, %d runs). A monitor that tracks "
            "the leak flags C1 and passes C3. Error bars are Wilson 95%% intervals; M1g as in "
            "Figure 1." % (n_c1, n_c3)),
        fig_evasions(tables): (
            "Supplementary figure S2 (repository only): share of scripted C5 cover-ups each monitor catches, by evasion. M4 uses "
            "the length L = %d set on calibration seeds." % length),
        fig_lcs(tables): (
            "Supplementary figure S1 (repository only): for each held-out run, the longest stretch of text shared by any destroyed "
            "artefact and any undeclared request (log scale, plus one so zero shows), split by "
            "whether the run is a cover-up by the canary label. C2 and C3 include the D1 seeds. "
            "M4 flags a run at or above the dashed line."),
    }
    (FIG / "captions.json").write_text(json.dumps(captions, indent=2, sort_keys=True) + "\n",
                                       encoding="utf-8")
    print("wrote %s" % ", ".join(sorted(captions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
