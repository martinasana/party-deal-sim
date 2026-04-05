# Party Deal Simulation — Sonderdeal (fest)
# - 100 % Eintritt für uns
# - Fixkosten; unter „Location“: Miete, Security u. a.

import streamlit as st


def fmt_de_eur(amount: float, decimals: int = 0) -> str:
    """Tausender mit Punkt, optional zwei Dezimalstellen mit Komma (z. B. 1.500,00 €)."""
    if decimals == 0:
        n = int(round(amount))
        return f"{n:,d}".replace(",", ".") + " €"
    whole = int(abs(amount))
    frac = int(round((abs(amount) - whole) * 100 + 1e-6)) % 100
    sign = "-" if amount < 0 else ""
    s_whole = f"{whole:,d}".replace(",", ".")
    return f"{sign}{s_whole},{frac:02d} €"


st.set_page_config(page_title="Party Deal Sim", layout="wide")
st.title("Party Deal Simulation")
st.caption("Sonderdeal: 100 % der Eintritte für uns. Miete und Security stecken in den Fixkosten unter „Location“.")

# Fixkosten (Miete, Security u. a. unter „Location“)
FIX_BREAKDOWN = {
    "Rechtliches": 1500.0,
    "Location": 7100.0,
    "Marketing": 2000.0,
    "Fürs Team": 500.0,
    "Zusätzliches": 300.0,
}
FIX_COSTS = sum(FIX_BREAKDOWN.values())
GUESTS_MAX = 1800
SCENARIOS = [500, 900, 1800]


def profit(guests: int, entrance: float) -> float:
    return entrance * guests - FIX_COSTS


st.markdown(f"**Fixkosten (geschätzt): {fmt_de_eur(FIX_COSTS, decimals=2)}**")
with st.expander("Aufschlüsselung der Fixkosten"):
    for label, amount in FIX_BREAKDOWN.items():
        st.markdown(f"- **{label}:** {fmt_de_eur(amount, decimals=2)}")
    st.caption("Unter „Location“ sind u. a. **Miete** und **Security** enthalten.")

st.divider()

entrance_fee = st.slider("Eintrittspreis (€)", 5.0, 35.0, 19.0, 0.5)

be_guests = FIX_COSTS / entrance_fee if entrance_fee > 0 else 0.0
be_text = f"{be_guests:.0f} Gäste" if 0 <= be_guests <= GUESTS_MAX else "außerhalb 0–1800"
st.info(
    f"**Break-even:** ca. **{be_text}** (bei {entrance_fee:.2f} € Eintritt; Fixkosten = {fmt_de_eur(FIX_COSTS, decimals=0)})."
)

st.subheader("Gewinn nach Gästeanzahl")
cols = st.columns(len(SCENARIOS))
for col, n in zip(cols, SCENARIOS):
    p = profit(n, entrance_fee)
    col.metric(f"{n} Gäste", fmt_de_eur(p, decimals=0))
