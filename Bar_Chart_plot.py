"""
Plot: Maximum Base Shear & Overturning Moment Comparison
With LRB vs Without LRB — Mean ± 16th–84th Percentile Band

CSV format expected (With LRB or Without LRB):
    RSN, PGA (g), Maximum Base Shear (kN), Maximum Overturning Moment (kN·m), ...

What is plotted:
  - X-axis : PGA Intensity Bins  [0–0.15g, 0.15–0.35g, 0.35–0.75g, 0.75–1.5g, 1.5–3.6g]
  - Y-axis  : Mean of the maximum response quantity across all ground-motion records
               that fall inside each PGA bin
  - Error bar: 16th percentile (lower cap) and 84th percentile (upper cap),
               representing the record-to-record variability band (≈ ±1 log-std)
  - Bar labels: mean value printed at the bar mid-height

Two side-by-side subplots:
  Left  → Maximum Base Shear (kN)
  Right → Maximum Overturning Moment (MN·m)  [converted from kN·m]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── 0. CONFIGURATION ──────────────────────────────────────────────────────────
WITH_LRB_CSV    = "100kL With LRB NLTHA A.csv"    # ← path to your "with LRB" CSV
WITHOUT_LRB_CSV = "100kL Without LRB NLTHA A.csv" # ← path to your "without LRB" CSV
OUTPUT_PNG      = "Baseshear_otm_comparison_for_soil_type_A_100KL.pdf"

# PGA bins: (label, low, high)
BINS = [
    ("0–0.15g",   0.00, 0.15),
    ("0.15–0.35g",0.15, 0.35),
    ("0.35–0.75g",0.35, 0.75),
    ("0.75–1.5g", 0.75, 1.50),
    ("1.5–3.6g",  1.50, 3.60),
]
BIN_LABELS = [b[0] for b in BINS]
N_BINS     = len(BINS)

# Columns of interest (exact names as they appear in the CSV header)
COL_PGA  = "PGA (g)"
COL_BS   = "Maximum Base Shear (kN)"
COL_OTM  = "Maximum Overturning Moment (kN·m)"  # will be converted to MN·m

# Colours
COLOR_WITHOUT = "#d62728"   # red
COLOR_WITH    = "#1f77b4"   # blue

# ── 1. HELPER: load CSV & assign bin index ────────────────────────────────────
def load_and_bin(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Rename OTM column robustly (handles encoding quirks in the header byte)
    otm_col = [c for c in df.columns if "Overturning" in c][0]
    df = df.rename(columns={otm_col: COL_OTM})

    # Convert OTM kN·m → MN·m
    df[COL_OTM] = df[COL_OTM] / 1_000.0

    # Assign bin
    def assign_bin(pga):
        for i, (_, lo, hi) in enumerate(BINS):
            if lo <= pga < hi:
                return i
        return -1   # outside range

    df["bin"] = df[COL_PGA].apply(assign_bin)
    df = df[df["bin"] >= 0]          # drop out-of-range records
    return df


# ── 2. HELPER: compute mean / p16 / p84 per bin ───────────────────────────────
def bin_stats(df: pd.DataFrame, col: str):
    means, p16s, p84s = [], [], []
    for i in range(N_BINS):
        vals = df.loc[df["bin"] == i, col].values
        if len(vals) == 0:
            means.append(np.nan); p16s.append(np.nan); p84s.append(np.nan)
        else:
            means.append(np.mean(vals))
            p16s.append(np.percentile(vals, 16))
            p84s.append(np.percentile(vals, 84))
    return np.array(means), np.array(p16s), np.array(p84s)


# ── 3. LOAD DATA ──────────────────────────────────────────────────────────────
df_with    = load_and_bin(WITH_LRB_CSV)

# If you don't have the Without-LRB CSV yet, comment the next line and
# the Without-LRB bars simply won't appear.
try:
    df_without = load_and_bin(WITHOUT_LRB_CSV)
    have_without = True
except FileNotFoundError:
    print(f"[WARNING] '{WITHOUT_LRB_CSV}' not found – plotting With-LRB only.")
    have_without = False


# ── 4. COMPUTE STATISTICS ─────────────────────────────────────────────────────
bs_with_mean,  bs_with_p16,  bs_with_p84  = bin_stats(df_with,    COL_BS)
otm_with_mean, otm_with_p16, otm_with_p84 = bin_stats(df_with,    COL_OTM)

if have_without:
    bs_wo_mean,  bs_wo_p16,  bs_wo_p84  = bin_stats(df_without, COL_BS)
    otm_wo_mean, otm_wo_p16, otm_wo_p84 = bin_stats(df_without, COL_OTM)


# ── 5. PLOT ───────────────────────────────────────────────────────────────────
x      = np.arange(N_BINS)
width  = 0.35          # bar width
offset = width / 2     # half-width offset for side-by-side placement

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
fig.suptitle(
    "Base Shear & Overturning Moment Comparison — With LRB vs Without LRB for 100KL capacity Tank with Soil Type A \n"
    "Mean ± 16th–84th Percentile Band across Ground Motion Records",
    fontsize=13, fontweight="bold"
)


def draw_bars(ax, wo_mean, wo_p16, wo_p84,
                  wi_mean, wi_p16, wi_p84,
                  ylabel, title, have_without=True):
    """Draw grouped bars with error bars and value labels."""

    if have_without:
        wo_yerr = np.array([wo_mean - wo_p16, wo_p84 - wo_mean])
        bars_wo = ax.bar(
            x - offset, wo_mean, width,
            color=COLOR_WITHOUT, label="Without LRB",
            yerr=wo_yerr, capsize=5,
            error_kw=dict(ecolor="black", elinewidth=1.2, capthick=1.2),
            zorder=3
        )

    wi_yerr = np.array([wi_mean - wi_p16, wi_p84 - wi_mean])
    bars_wi = ax.bar(
        x + (offset if have_without else 0), wi_mean, width,
        color=COLOR_WITH, label="With LRB",
        yerr=wi_yerr, capsize=5,
        error_kw=dict(ecolor="black", elinewidth=1.2, capthick=1.2),
        zorder=3
    )

    # Value labels on bars
    def label_bars(bars, values):
        for bar, val in zip(bars, values):
            if np.isnan(val):
                continue
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 0.5,          # mid-height
                f"{val:.0f}" if val > 10 else f"{val:.1f}",
                ha="center", va="center",
                fontsize=8.5, fontweight="bold", color="white"
            )

    if have_without:
        label_bars(bars_wo, wo_mean)
    label_bars(bars_wi, wi_mean)

    # Formatting
    ax.set_xticks(x)
    ax.set_xticklabels(BIN_LABELS, fontsize=10)
    ax.set_xlabel("PGA Intensity Bin", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)


# -- Base Shear ---------------------------------------------------------------
draw_bars(
    ax1,
    bs_wo_mean if have_without else None,
    bs_wo_p16  if have_without else None,
    bs_wo_p84  if have_without else None,
    bs_with_mean, bs_with_p16, bs_with_p84,
    ylabel="Mean Maximum Base Shear (kN)",
    title="Maximum Base Shear",
    have_without=have_without
)

# -- Overturning Moment -------------------------------------------------------
draw_bars(
    ax2,
    otm_wo_mean if have_without else None,
    otm_wo_p16  if have_without else None,
    otm_wo_p84  if have_without else None,
    otm_with_mean, otm_with_p16, otm_with_p84,
    ylabel="Mean Maximum Overturning Moment (MN·m)",
    title="Maximum Overturning Moment",
    have_without=have_without
)

plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches="tight")
print(f"Saved → {OUTPUT_PNG}")
plt.show()