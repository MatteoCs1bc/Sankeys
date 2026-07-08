import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")
st.markdown("Rappresentazione del peso percentuale delle fonti sul totale delle importazioni.")

# ----------------------------------------------------
# 1. Definizione delle etichette (Nodi) con le percentuali incorporate
# ----------------------------------------------------
# A Sinistra: Il Mix del 2020 (Totale 100%)
# A Destra: Il Mix del 2025 (Totale 100%)

label = [
    # Nodi 2020 (Indici 0-5)
    "Russia (43.4%)",           # 0
    "Algeria (18.5%)",          # 1
    "GNL via Nave (20.0%)",     # 2
    "Nord Europa (11.5%)",      # 3
    "Libia (6.7%)",             # 4
    "Azerbaigian (0%)",         # 5
    
    # Nodi 2025 (Indici 6-11)
    "Russia (1.3%)",            # 6
    "Algeria (32.8%)",          # 7
    "GNL via Nave (34.1%)",     # 8
    "Nord Europa (14.0%)",      # 9
    "Libia (1.5%)",             # 10
    "Azerbaigian (16.3%)"       # 11
]

# ----------------------------------------------------
# 2. Definizione dei Flussi (Diretti da Sinistra a Destra)
# ----------------------------------------------------
# Colleghiamo direttamente il paese del 2020 al paese del 2025.
# Il "valore" del flusso (lo spessore) sarà determinato dalla percentuale FINALE (2025)
# in modo che lo spessore a destra corrisponda alla situazione attuale. 
# Per i flussi in diminuzione (es. Russia), lo spessore si adatta automaticamente.

source = [0,   1,    2,    3,    4,    5]     # Da: Nodi 2020
target = [6,   7,    8,    9,    10,   11]    # A: Nodi 2025

# Usiamo come spessore di transizione la media visiva o direttamente il valore del 2025
# Affinché si capisca lo "spostamento" usiamo il mix del 2025 come valore di destinazione.
# (Per permettere al nodo 0% dell'Azerbaigian di essere collegato visivamente, mettiamo un valore micro).
value =  [1.3, 32.8, 34.1, 14.0, 1.5, 16.3]

# ----------------------------------------------------
# 3. Colori 
# ----------------------------------------------------
node_colors = [
    "#d62728", # 0 Russia
    "#2ca02c", # 1 Algeria
    "#9467bd", # 2 GNL
    "#e377c2", # 3 Nord Europa
    "#8c564b", # 4 Libia
    "#17becf", # 5 Azerbaigian (Trasparente nel 2020)
    
    "#d62728", # 6 Russia
    "#2ca02c", # 7 Algeria
    "#9467bd", # 8 GNL
    "#e377c2", # 9 Nord Europa
    "#8c564b", # 10 Libia
    "#17becf"  # 11 Azerbaigian
]

# Colori semi-trasparenti per i flussi di collegamento
link_colors = [
    "rgba(214, 39, 40, 0.4)",  # Flusso Russia
    "rgba(44, 160, 44, 0.4)",  # Flusso Algeria
    "rgba(148, 103, 189, 0.4)",# Flusso GNL
    "rgba(227, 119, 194, 0.4)",# Flusso Nord Europa
    "rgba(140, 86, 75, 0.4)",  # Flusso Libia
    "rgba(23, 190, 207, 0.4)"  # Flusso Azerbaigian
]

# ----------------------------------------------------
# 4. Creazione Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="snap", # Mantiene i nodi allineati il più possibile
    node = dict(
      pad = 30,
      thickness = 40,
      line = dict(color = "black", width = 0.5),
      label = label,
      color = node_colors
    ),
    link = dict(
      source = source,
      target = target,
      value = value,
      color = link_colors
  ))])

fig.update_layout(
    height=650, 
    margin=dict(t=30, b=30, l=20, r=20),
    font=dict(size=13)
)

# Aggiungiamo delle annotazioni per chiarire le colonne
fig.add_annotation(x=0, y=-0.1, text="<b>Mix Import 2020</b>", showarrow=False, font=dict(size=16))
fig.add_annotation(x=1, y=-0.1, text="<b>Mix Import 2025</b>", showarrow=False, font=dict(size=16))

st.plotly_chart(fig, use_container_width=True)
