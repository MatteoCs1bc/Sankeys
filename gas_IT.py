import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")
st.markdown("Valori in **Miliardi di metri cubi (Gmc)** e peso percentuale.")

# ----------------------------------------------------
# 1. Definizione delle etichette (Nodi)
# ----------------------------------------------------
label = [
    # Nodi 2020 (0-4)
    "Russia (28.4 Gmc | 43.4%)", 
    "Algeria (12.1 Gmc | 18.5%)", 
    "GNL (USA, Qatar, Algeria) (13.1 Gmc | 20.0%)", 
    "Nord Europa (7.5 Gmc | 11.5%)", 
    "Libia (4.4 Gmc | 6.7%)", 
    
    # Nodi Centrali (5, 6)
    "Sistema Gas Italia", 
    "Calo Import (-4.2 Gmc)", 
    
    # Nodi 2025 (7-12)
    "Russia (0.8 Gmc | 1.3%)", 
    "Algeria (20.1 Gmc | 32.8%)", 
    "GNL (USA, Qatar, Algeria) (20.9 Gmc | 34.1%)", 
    "Nord Europa (8.6 Gmc | 14.0%)", 
    "Libia (0.9 Gmc | 1.5%)", 
    "Azerbaigian (10.0 Gmc | 16.3%)"
]

# ----------------------------------------------------
# 2. Forzatura delle Coordinate (X e Y) per mantenere l'ordine
# ----------------------------------------------------
# Usando x e y possiamo dire a Plotly ESATTAMENTE dove piazzare i blocchi,
# in modo che Russia sia sempre in alto e l'ordine rimanga identico.
x_pos = [
    0.01, 0.01, 0.01, 0.01, 0.01,  # 0-4: Sinistra (2020)
    0.5,                           # 5: Sistema Italia (Centro)
    0.5,                           # 6: Calo Import (Centro)
    0.99, 0.99, 0.99, 0.99, 0.99, 0.99 # 7-12: Destra (2025)
]

y_pos = [
    0.15, 0.35, 0.55, 0.75, 0.90,  # 0-4: Paesi 2020 in ordine
    0.01,                          # 5: Sistema Italia FORZATO IN ALTO (Sopra)
    0.99,                          # 6: Calo Import FORZATO IN BASSO (Sotto)
    0.15, 0.35, 0.55, 0.75, 0.90, 0.99 # 7-12: Paesi 2025 nello stesso ordine
]

# ----------------------------------------------------
# 3. Logica dei flussi
# ----------------------------------------------------
source = [
    0, 1, 2, 3, 4,    # Da: Paesi 2020 -> Italia
    5,                # Da: Italia -> Calo Import
    5, 5, 5, 5, 5, 5  # Da: Italia -> Paesi 2025
]

target = [
    5, 5, 5, 5, 5,    # A: Italia Centrale
    6,                # A: Calo Import
    7, 8, 9, 10, 11, 12 # A: Paesi 2025
]

value = [
    28.4, 12.1, 13.1, 7.5, 4.4, # Volumi in ingresso 2020
    4.2,                        # Volume del calo
    0.8, 20.1, 20.9, 8.6, 0.9, 10.0 # Volumi in uscita verso il mix 2025
]

# ----------------------------------------------------
# 4. Colori 
# ----------------------------------------------------
node_colors = [
    # Colori 2020
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b",
    # Colori Centrali
    "#1f77b4", "#7f7f7f",
    # Colori 2025
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b", "#17becf"
]

link_colors = [
    # Ingressi 2020
    "rgba(214, 39, 40, 0.4)",   
    "rgba(44, 160, 44, 0.4)",   
    "rgba(148, 103, 189, 0.4)", 
    "rgba(227, 119, 194, 0.4)", 
    "rgba(140, 86, 75, 0.4)",   
    
    # Uscite verso Calo
    "rgba(150, 150, 150, 0.5)",
    
    # Uscite verso 2025
    "rgba(214, 39, 40, 0.4)",   
    "rgba(44, 160, 44, 0.4)",   
    "rgba(148, 103, 189, 0.4)", 
    "rgba(227, 119, 194, 0.4)", 
    "rgba(140, 86, 75, 0.4)",   
    "rgba(23, 190, 207, 0.4)"   
]

# ----------------------------------------------------
# 5. Creazione Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="freeform", # Permette il posizionamento manuale
    node = dict(
      pad = 20,
      thickness = 35,
      line = dict(color = "black", width = 0.5),
      label = label,
      color = node_colors,
      x = x_pos,
      y = y_pos
    ),
    link = dict(
      source = source,
      target = target,
      value = value,
      color = link_colors
  ))])

fig.update_layout(
    height=800, 
    margin=dict(t=50, b=50, l=20, r=20),
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)
