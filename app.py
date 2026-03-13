# Party Deal Simulation
# - Guest counts 0–1800, plot profit vs guests
# - Fixed costs (excl. rent): 3500€ | Entrance fee: configurable
# - Deal 1: 8000€ rent, 100% entrance fees to us
# - Deal 2: no rent, doordeal:60% entrance fees to us, 40% to venue
# - Deal 3: special deal, only fee for 4000, security from us 2000€

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Party Deal Sim", layout="wide")
st.title("Party Deal Simulation")

FIX_COSTS = 3500
RENT_DEAL1 = 8000
DEAL2_SHARE = 0.6
GUESTS_MAX = 1800
DEAL3_FEE = 4000  # Gebühr an Location
DEAL3_EXTRA = 2000  # Security (+ ggf. Garderobe) von uns

entrance_fee = st.slider("Eintrittspreis (€)", 5.0, 35.0, 19.0, 0.5)

# Checkboxen: Deals im Graphen ein-/ausblenden
show_deal1 = st.checkbox("Standard Deal anzeigen (Miete 8000€, 100% Eintritt – stand ursprünglich im Raum)", value=True)
show_deal2 = st.checkbox("Door Deal anzeigen (keine Miete, 60% Eintritt für uns - 40% für die Location)", value=True)
show_deal3 = st.checkbox("Benefit Deal anzeigen (Miete 4000€ + 2000€ Security selbst, 100% Eintritt – ausgehandelt)", value=True)
show_scenarios = st.checkbox("Szenarios anzeigen (500 / 900 / 1800 Gäste im Graph)", value=True)

guests = np.arange(0, GUESTS_MAX + 1, 10)
revenue1 = entrance_fee * guests
profit1 = revenue1 - RENT_DEAL1 - FIX_COSTS
profit2 = (entrance_fee * guests * DEAL2_SHARE) - FIX_COSTS
profit3 = revenue1 - DEAL3_FEE - FIX_COSTS - DEAL3_EXTRA

# Break-even (nur textuell, nicht im Graphen)
be_guests_1 = (RENT_DEAL1 + FIX_COSTS) / entrance_fee if entrance_fee > 0 else 0
be_guests_2 = FIX_COSTS / (entrance_fee * DEAL2_SHARE) if entrance_fee > 0 else 0
be_guests_3 = (DEAL3_FEE + FIX_COSTS + DEAL3_EXTRA) / entrance_fee if entrance_fee > 0 else 0
be_text_1 = f"{be_guests_1:.0f} Gäste" if 0 <= be_guests_1 <= GUESTS_MAX else "außerhalb 0–1800"
be_text_2 = f"{be_guests_2:.0f} Gäste" if 0 <= be_guests_2 <= GUESTS_MAX else "außerhalb 0–1800"
be_text_3 = f"{be_guests_3:.0f} Gäste" if 0 <= be_guests_3 <= GUESTS_MAX else "außerhalb 0–1800"
st.caption(f"**Break-even:** Standard: {be_text_1} · Door Deal: {be_text_2} · Benefit Deal: {be_text_3}")

# Farben für Graph und Tabelle (abgestimmt)
COLOR_STANDARD = "#1f77b4"
COLOR_DOOR = "#ff7f0e"
COLOR_BENEFIT = "#2ca02c"
BG_STANDARD = "#d4e8f7"
BG_DOOR = "#ffe4cc"
BG_BENEFIT = "#dcf5dc"

SCENARIOS = [500, 900, 1800]

fig, ax = plt.subplots(figsize=(10, 5))
if show_deal1:
    ax.plot(guests, profit1, label="Standard (Miete 8000€, 100% Eintritt)", color=COLOR_STANDARD)
if show_deal2:
    ax.plot(guests, profit2, label="Door Deal (keine Miete, 60% Eintritt)", color=COLOR_DOOR)
if show_deal3:
    ax.plot(guests, profit3, label="Benefit Deal (Gebühr 4000€ + 2000€, 100% Eintritt)", color=COLOR_BENEFIT)

# Szenario-Punkte (500, 900, 1800 Gäste) pro Deal – nur wenn aktiviert
if show_scenarios:
    def p1(n): return entrance_fee * n - RENT_DEAL1 - FIX_COSTS
    def p2(n): return entrance_fee * n * DEAL2_SHARE - FIX_COSTS
    def p3(n): return entrance_fee * n - DEAL3_FEE - FIX_COSTS - DEAL3_EXTRA
    deals = [
        (show_deal1, profit1, p1, "Standard", COLOR_STANDARD),
        (show_deal2, profit2, p2, "Door", COLOR_DOOR),
        (show_deal3, profit3, p3, "Benefit", COLOR_BENEFIT),
    ]
    for show, profit_curve, profit_fn, name, color in deals:
        if not show:
            continue
        xs, ys = [], []
        for n in SCENARIOS:
            xs.append(n)
            ys.append(profit_fn(n))
        ax.scatter(xs, ys, color=color, s=40, zorder=5, edgecolors="white", linewidths=1)
        for n in SCENARIOS:
            y = profit_fn(n)
            ax.annotate(f"{name} ({n}, {y:.0f})", (n, y), xytext=(5, 5), textcoords="offset points", fontsize=7, color=color)

ax.axhline(0, color="gray", linestyle="--", linewidth=1)
ax.axvline(500, color="gray", linestyle="-.", alpha=0.5)
ax.axvline(900, color="gray", linestyle="-.", alpha=0.5)
ax.axvline(1800, color="gray", linestyle="-.", alpha=0.5)
ax.set_xlabel("Gästeanzahl")
ax.set_ylabel("Gewinn (€)")
ax.set_title("Gewinn vs. Gästeanzahl")
ax.legend(loc="best", fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig)
plt.close()

# Szenarien tabellarisch mit farbiger Zuordnung zu den Deals
st.subheader("Szenarien: Gewinn nach Gästeanzahl")
SCENARIOS = [500, 900, 1800]

def profit_standard(n): return entrance_fee * n - RENT_DEAL1 - FIX_COSTS
def profit_door(n): return entrance_fee * n * DEAL2_SHARE - FIX_COSTS
def profit_benefit(n): return entrance_fee * n - DEAL3_FEE - FIX_COSTS - DEAL3_EXTRA

# Tabelle als HTML für zuverlässige Farben (Streamlit-DataFrame-Styling ist oft ignoriert)
rows = [
    ("Standard", COLOR_STANDARD, profit_standard(500), profit_standard(900), profit_standard(1800)),
    ("Door Deal", COLOR_DOOR, profit_door(500), profit_door(900), profit_door(1800)),
    ("Benefit Deal", COLOR_BENEFIT, profit_benefit(500), profit_benefit(900), profit_benefit(1800)),
]
cell_base = "padding: 0.5rem 0.75rem; text-align: right; color: #1a1a1a; background: #f8f9fa;"
header_style = "padding: 0.5rem 0.75rem; text-align: right; color: #1a1a1a; background: #e9ecef; font-weight: 600;"
table_html = f"""
<table style="width:100%; border-collapse: separate; border-spacing: 0 8px; font-size: 0.95rem;">
  <thead><tr>
    <th style="{header_style} text-align: left;">Deal</th>
    <th style="{header_style}">500 Gäste</th>
    <th style="{header_style}">900 Gäste</th>
    <th style="{header_style}">1800 Gäste</th>
  </tr></thead>
  <tbody>
"""
for name, border_color, v500, v900, v1800 in rows:
    # Komplette Zeile umranden: Rand pro Zelle, damit die ganze Zeile farbig eingerahmt ist
    b = f"6px solid {border_color}"
    td_first = f"{cell_base} text-align: left; border-left: {b}; border-top: {b}; border-bottom: {b};"
    td_mid   = f"{cell_base} border-top: {b}; border-bottom: {b};"
    td_last  = f"{cell_base} border-right: {b}; border-top: {b}; border-bottom: {b};"
    table_html += f"""
  <tr>
    <td style="{td_first}">{name}</td>
    <td style="{td_mid}">{v500:,.0f} €</td>
    <td style="{td_mid}">{v900:,.0f} €</td>
    <td style="{td_last}">{v1800:,.0f} €</td>
  </tr>
"""
table_html += "  </tbody>\n</table>"
st.markdown(table_html, unsafe_allow_html=True)
