import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")
st.markdown("Rappresentazione del peso percentuale delle fonti sul totale delle importazioni.")

# ----------------------------------------------------
# 1. Definizione delle etichette (Nodi)
# ----------------------------------------------------
label = [
    # Nodi 2020 (0-5)
    "Russia (43.4%)", 
    "Algeria (18.5%)", 
    "GNL via Nave (USA, Qatar, Algeria) (20.0%)", 
    "Nord Europa (11.5%)", 
    "Libia (6.7%)", 
    "Azerbaigian (0%)",
    
    # Nodi 2025 (6-11)
    "Russia (1.3%)", 
    "Algeria (32.8%)", 
    "GNL via Nave (USA, Qatar, Algeria) (34.1%)", 
    "Nord Europa (14.0%)", 
    "Libia (1.5%)", 
    "Azerbaigian (16.3%)",
    
    # Nodi INVISIBILI per bilanciare la matematica senza sporcare il grafico (12, 13)
    " ", " "
]

# ----------------------------------------------------
# 2. Logica dei flussi e "Trucco" della Trasparenza
# ----------------------------------------------------
source = []
target = []
value = []
link_colors = []

vals_2020 = [43.4, 18.5, 20.0, 11.5, 6.7, 0.1]
vals_2025 = [1.3, 32.8, 34.1, 14.0, 1.5, 16.3]

base_colors = [
    "rgba(214, 39, 40, 0.6)",   # Russia (Rosso)
    "rgba(44, 160, 44, 0.6)",   # Algeria (Verde)
    "rgba(148, 103, 189, 0.6)", # GNL (Viola)
    "rgba(227, 119, 194, 0.6)", # Nord Europa (Rosa)
    "rgba(140, 86, 75, 0.6)",   # Libia (Marrone)
    "rgba(23, 190, 207, 0.6)"   # Azerbaigian (Ciano)
]

for i in range(6):
    min_val = min(vals_2020[i], vals_2025[i])
    
    # Flusso visibile Paese-Paese
    source.append(i)
    target.append(i+6)
    value.append(min_val)
    link_colors.append(base_colors[i])
    
    # Flussi invisibili per bilanciare le percentuali
    if vals_2020[i] > vals_2025[i]:
        source.append(i)
        target.append(13)
        value.append(vals_2020[i] - min_val)
        link_colors.append("rgba(0,0,0,0)") # 100% Trasparente
    elif vals_2025[i] > vals_2020[i]:
        source.append(12)
        target.append(i+6)
        value.append(vals_2025[i] - min_val)
        link_colors.append("rgba(0,0,0,0)") # 100% Trasparente

# ----------------------------------------------------
# 3. Colori dei Nodi
# ----------------------------------------------------
node_colors = [
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b", "#17becf", # Sinistra
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b", "#17becf", # Destra
    "rgba(0,0,0,0)", "rgba(0,0,0,0)" # Nodi invisibili
]

node_line_colors = ["black"] * 12 + ["rgba(0,0,0,0)", "rgba(0,0,0,0)"]
node_line_widths = [0.5] * 12 + [0, 0]

# ----------------------------------------------------
# 4. Creazione Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="perpendicular",
    node = dict(
      pad = 25,
      thickness = 35,
      line = dict(color = node_line_colors, width = node_line_widths),
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
    height=750, 
    margin=dict(t=50, b=50, l=20, r=20),
    font=dict(size=14)
)

fig.add_annotation(x=0.0, y=1.05, text="<b>Import 2020</b>", showarrow=False, font=dict(size=18), xref="paper", yref="paper")
fig.add_annotation(x=1.0, y=1.05, text="<b>Import 2025</b>", showarrow=False, font=dict(size=18), xref="paper", yref="paper")

st.plotly_chart(fig, use_container_width=True)
