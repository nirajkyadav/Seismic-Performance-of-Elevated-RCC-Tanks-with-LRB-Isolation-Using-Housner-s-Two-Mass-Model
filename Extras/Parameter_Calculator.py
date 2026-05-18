import math

# ─────────────────────────────────────────────────────────────
#   Circular Tank – Sloshing Parameter Calculator
#   Inputs : h  = liquid height (m)
#            D  = tank diameter (m)
#            m  = total liquid mass (kg)   [needed for K_c]
#            g  = gravitational acceleration (m/s²), default 9.81
# ─────────────────────────────────────────────────────────────

def circular_tank_sloshing(h, D, m, g=9.81):
    """
    Calculate sloshing parameters for a circular tank.

    Parameters
    ----------
    h : float  – Liquid height (m)
    D : float  – Tank diameter (m)
    m : float  – Total liquid mass (kg)
    g : float  – Gravitational acceleration (m/s²), default 9.81

    Returns
    -------
    dict with all computed ratios and K_c
    """

    ratio_h_D = h / D   # h/D
    ratio_D_h = D / h   # D/h

    # ── 1. Impulsive mass ratio  m_i / m ─────────────────────
    arg_i = 0.866 * ratio_D_h
    mi_over_m = math.tanh(arg_i) / arg_i

    # ── 2. Impulsive height ratio  h_i / h ───────────────────
    if ratio_h_D <= 0.75:
        hi_over_h = 0.375
    else:
        hi_over_h = 0.5 - (0.09375 / ratio_h_D)

    # ── 3. Impulsive height ratio (with base pressure)  h_i* / h ──
    if ratio_h_D <= 1.33:
        hi_star_over_h = arg_i / (2 * math.tanh(arg_i)) - 0.125
    else:
        hi_star_over_h = 0.45

    # ── 4. Convective mass ratio  m_c / m ────────────────────
    arg_c = 3.68 * ratio_h_D
    mc_over_m = 0.23 * math.tanh(arg_c) / ratio_h_D

    # ── 5. Convective height ratio  h_c / h ──────────────────
    hc_over_h = 1.0 - (math.cosh(arg_c) - 1.0) / (3.68 * ratio_h_D * math.sinh(arg_c))

    # ── 6. Convective height ratio (with base pressure)  h_c* / h ──
    hc_star_over_h = 1.0 - (math.cosh(arg_c) - 2.01) / (3.68 * ratio_h_D * math.sinh(arg_c))

    # ── 7. Convective spring stiffness  K_c ──────────────────
    Kc = 0.836 * (m * g / h) * (math.tanh(arg_c) ** 2)

    # ── 8. Actual masses and heights ──────────────────────────
    mi = mi_over_m * m
    mc = mc_over_m * m
    hi = hi_over_h * h
    hi_star = hi_star_over_h * h
    hc = hc_over_h * h
    hc_star = hc_star_over_h * h

    return {
        "h/D"          : ratio_h_D,
        "D/h"          : ratio_D_h,
        # --- ratios ---
        "mi/m"         : mi_over_m,
        "hi/h"         : hi_over_h,
        "hi*/h"        : hi_star_over_h,
        "mc/m"         : mc_over_m,
        "hc/h"         : hc_over_h,
        "hc*/h"        : hc_star_over_h,
        # --- actual values ---
        "mi (kg)"      : mi,
        "mc (kg)"      : mc,
        "hi (m)"       : hi,
        "hi* (m)"      : hi_star,
        "hc (m)"       : hc,
        "hc* (m)"      : hc_star,
        "Kc (N/m)"     : Kc,
    }


# ─────────────────────────────────────────────────────────────
#   Main – user input
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("   Circular Tank – Sloshing Parameter Calculator")
    print("=" * 50)

    h = float(input("Enter liquid height  h  (m) : "))
    D = float(input("Enter tank diameter  D  (m) : "))
    m = float(input("Enter liquid mass    m (kg) : "))
    g_input = input("Enter gravity g (m/s²) [press Enter for 9.81] : ")
    g = float(g_input) if g_input.strip() else 9.81

    if h <= 0 or D <= 0 or m <= 0:
        print("\n[ERROR] h, D, and m must all be positive numbers.")
    else:
        results = circular_tank_sloshing(h, D, m, g)

        print("\n" + "=" * 50)
        print("   Results")
        print("=" * 50)
        print(f"  h / D                      = {results['h/D']:.4f}")
        print(f"  D / h                      = {results['D/h']:.4f}")
        print("-" * 50)
        print(f"  {'Parameter':<28} {'Ratio':>10}   {'Actual Value':>15}")
        print("-" * 60)
        print(f"  {'mi/m  →  mi (kg)':<28} {results['mi/m']:>10.4f}   {results['mi (kg)']:>12.4f} kg")
        print(f"  {'hi/h  →  hi (m)':<28} {results['hi/h']:>10.4f}   {results['hi (m)']:>12.4f} m")
        print(f"  {'hi*/h →  hi* (m)':<28} {results['hi*/h']:>10.4f}   {results['hi* (m)']:>12.4f} m")
        print("-" * 60)
        print(f"  {'mc/m  →  mc (kg)':<28} {results['mc/m']:>10.4f}   {results['mc (kg)']:>12.4f} kg")
        print(f"  {'hc/h  →  hc (m)':<28} {results['hc/h']:>10.4f}   {results['hc (m)']:>12.4f} m")
        print(f"  {'hc*/h →  hc* (m)':<28} {results['hc*/h']:>10.4f}   {results['hc* (m)']:>12.4f} m")
        print("-" * 60)
        print(f"  Convective stiffness Kc    = {results['Kc (N/m)']:.4f}  N/m")
        print("=" * 60)
