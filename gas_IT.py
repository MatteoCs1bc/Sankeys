import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")

# ----------------------------------------------------
# Definizione dei Nodi
# ----------------------------------------------------
# Ordine degli indici:
# 0-4: Paesi 2020 (Sinistra)
# 5: Nodo Centrale "Sistema Italia" (Centro)
# 6-11: Paesi 2025 (Destra)

label = [
    # Sinistra: Flussi in entrata (2020)
    "Russia '20",       # 0
    "Algeria '20",      # 1
    "GNL '20",          # 2
    "Nord Europa '20",  # 3
    "Libia '20",        # 4
    
    # Centro
    "Sistema Gas Italia", # 5
    
    # Destra: Flussi proiettati/attuali (2025)
    "Russia '25",       # 6
    "Algeria '25",      # 7
    "GNL '25",          # 8
    "Nord Europa '25",  # 9
    "Libia '25",        # 10
    "Azerbaigian '25"   # 11
]

# ----------------------------------------------------
# Definizione dei Flussi (Sorgente -> Destinazione)
# ----------------------------------------------------
# Flussi del 2020: dai paesi (0,1,2,3,4) verso l'Italia (5)
source_2020 = [0, 1, 2, 3, 4]
target_2020 = [5, 5, 5, 5, 5]
value_2020  = [28.4, 12.1, 13.1, 7.5, 4.4]

# Flussi del 2025: in un Sankey standard il nodo centrale "spinge" 
# verso l'esterno. Quindi dall'Italia (5) verso i paesi del 2025 (6,7,8,9,10,11)
source_2025 = [5, 5, 5, 5, 5, 5]
target_2025 = [6, 7, 8, 9, 10, 11]
value_2025  = [0.8, 20.1, 20.9, 8.6, 0.9, 10.0]

# Uniamo le liste
source = source_2020 + source_2025
target = target_2020 + target_2025
value  = value_2020 + value_2025

# ----------------------------------------------------
# Colori personalizzati per capire bene il flusso
# ----------------------------------------------------
# Manteniamo la stessa tonalità per lo stesso paese tra 2020 e 2025
node_colors = [
    "#d62728", # Russia (Rosso)
    "#2ca02c", # Algeria (Verde)
    "#9467bd", # GNL (Viola)
    "#e377c2", # Nord Europa (Rosa)
    "#8c564b", # Libia (Marrone)
    
    "#1f77b4", # ITALIA CENTRALE (Blu)
    
    "#d62728", # Russia (Rosso)
    "#2ca02c", # Algeria (Verde)
    "#9467bd", # GNL (Viola)
    "#e377c2", # Nord Europa (Rosa)
    "#8c564b", # Libia (Marrone)
    "#17becf"  # Azerbaigian (Ciano) - non c'era nel 2020
]

# ----------------------------------------------------
# Creazione e Rendering del Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 25,
      thickness = 30,
      line = dict(color = "black", width = 0.5),
      label = label,
      color = node_colors
    ),
    link = dict(
      source = source,
      target = target,
      value = value,
      color = "rgba(200, 200, 200, 0.4)"
  ))])

fig.update_layout(
    height=600, 
    margin=dict(t=20, b=20, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
*Nota: Nel diagramma di Sankey i volumi centrali devono idealmente bilanciarsi. 
Nel 2020 l'Italia importava circa 65.5 Gmc. Nel 2025 ne importa circa 61.3 Gmc (a causa della riduzione dei consumi). 
Il nodo centrale rappresenta il "mix nazionale".*
""")
