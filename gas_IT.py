import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")
st.markdown("Rappresentazione del peso percentuale delle fonti sul totale delle importazioni. (GNL in larga parte da **Stati Uniti** e Qatar).")

# ----------------------------------------------------
# 1. Definizione delle etichette (Nodi)
# ----------------------------------------------------
label = [
    # Nodi 2020 (0-5)
    "Russia (43.4%)", "Algeria (18.5%)", "GNL via Nave (20.0%)", 
    "Nord Europa (11.5%)", "Libia (6.7%)", "Azerbaigian (0%)",
    
    # Nodi 2025 (6-11)
    "Russia (1.3%)", "Algeria (32.8%)", "GNL via Nave (34.1%)", 
    "Nord Europa (14.0%)", "Libia (1.5%)", "Azerbaigian (16.3%)",
    
    # Nodi virtuali di bilanciamento per mantenere le proporzioni dei blocchi (12, 13)
    "Quote Compensate da nuove fonti (+)", "Quote Ridotte (-)"
]

# ----------------------------------------------------
# 2. Logica dei flussi proporzionali
# ----------------------------------------------------
source = []
target = []
value = []

vals_2020 = [43.4, 18.5, 20.0, 11.5, 6.7, 0.1] # 0.1 all'Azerbaigian solo per renderlo visibile nel 2020
vals_2025 = [1.3, 32.8, 34.1, 14.0, 1.5, 16.3]

for i in range(6):
    min_val = min(vals_2020[i], vals_2025[i])
    
    # 1. Flusso di MANTENIMENTO (Collega direttamente il paese 2020 al paese 2025)
    source.append(i)
    target.append(i+6)
    value.append(min_val)
    
    # 2. Flusso di DELTA (Se scende o se sale)
    if vals_2020[i] > vals_2025[i]:
        # Il paese ha perso quote (es. Russia, Libia): la differenza va al nodo "Quote Ridotte" (13)
        source.append(i)
        target.append(13)
        value.append(vals_2020[i] - min_val)
    elif vals_2025[i] > vals_2020[i]:
        # Il paese ha guadagnato quote (es. GNL, Algeria): la differenza arriva dal nodo "Quote Compensate" (12)
        source.append(12)
        target.append(i+6)
        value.append(vals_2025[i] - min_val)

# ----------------------------------------------------
# 3. Colori 
# ----------------------------------------------------
# Colori dei Nodi
node_colors = [
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b", "#17becf", # Sinistra
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b", "#17becf", # Destra
    "#e0e0e0", "#e0e0e0" # Nodi di bilanciamento in grigio chiaro
]

# Logica per i colori dei flussi
link_colors = []
for s, t in zip(source, target):
    if t == 13: # Flusso verso le quote perse (semitrasparente grigio)
        link_colors.append("rgba(200, 200, 200, 0.3)")
    elif s == 12: # Flusso dalle quote acquisite (semitrasparente grigio)
        link_colors.append("rgba(200, 200, 200, 0.3)")
    else:
        # Flussi diretti Paese-Paese (prendono il colore del paese)
        base_colors = ["rgba(214, 39, 40, 0.5)", "rgba(44, 160, 44, 0.5)", 
                       "rgba(148, 103, 189, 0.5)", "rgba(227, 119, 194, 0.5)", 
                       "rgba(140, 86, 75, 0.5)", "rgba(23, 190, 207, 0.5)"]
        link_colors.append(base_colors[s]) # s va da 0 a 5

# ----------------------------------------------------
# 4. Creazione Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="perpendicular", # Aiuta a disporre i nodi logici in colonne fisse
    node = dict(
      pad = 25,
      thickness = 35,
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
    height=750, 
    margin=dict(t=50, b=50, l=20, r=20),
    font=dict(size=14)
)

# Titoli delle due colonne
fig.add_annotation(x=0.0, y=1.05, text="<b>Import 2020</b>", showarrow=False, font=dict(size=18), xref="paper", yref="paper")
fig.add_annotation(x=1.0, y=1.05, text="<b>Import 2025</b>", showarrow=False, font=dict(size=18), xref="paper", yref="paper")

st.plotly_chart(fig, use_container_width=True)
