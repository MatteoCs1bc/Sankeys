import os

out_dir = "/tmp/user_code_sankey_3"
os.makedirs(out_dir, exist_ok=True)
file_path = os.path.join(out_dir, "gas_IT_v3.py")

code = """import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")
st.markdown("Valori in **Miliardi di metri cubi (Gmc)** e peso percentuale. Il nodo centrale mostra la transizione e il calo della domanda.")

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
    
    # Nodi Centrali (5, 6, 7)
    "Import Italia 2020 (65.5 Gmc)", 
    "Calo Import (-4.2 Gmc)", 
    "Import Italia 2025 (61.3 Gmc)", 
    
    # Nodi 2025 (8-13)
    "Russia (0.8 Gmc | 1.3%)", 
    "Algeria (20.1 Gmc | 32.8%)", 
    "GNL (USA, Qatar, Algeria) (20.9 Gmc | 34.1%)", 
    "Nord Europa (8.6 Gmc | 14.0%)", 
    "Libia (0.9 Gmc | 1.5%)", 
    "Azerbaigian (10.0 Gmc | 16.3%)"
]

# ----------------------------------------------------
# 2. Logica dei flussi
# ----------------------------------------------------
source = [
    0, 1, 2, 3, 4,    # Da: Paesi 2020 -> Italia 2020
    5,                # Da: Italia 2020 -> Calo Import
    5,                # Da: Italia 2020 -> Italia 2025
    7, 7, 7, 7, 7, 7  # Da: Italia 2025 -> Paesi 2025
]

target = [
    5, 5, 5, 5, 5,    # A: Italia 2020
    6,                # A: Calo Import
    7,                # A: Italia 2025
    8, 9, 10, 11, 12, 13 # A: Paesi 2025
]

value = [
    28.4, 12.1, 13.1, 7.5, 4.4, # Volumi in ingresso 2020
    4.2,                        # Volume del calo
    61.3,                       # Volume trasferito al 2025
    0.8, 20.1, 20.9, 8.6, 0.9, 10.0 # Volumi in uscita verso il mix 2025
]

# ----------------------------------------------------
# 3. Colori 
# ----------------------------------------------------
node_colors = [
    # Colori 2020
    "#d62728", "#2ca02c", "#9467bd", "#e377c2", "#8c564b",
    # Colori Centrali (Blu Italia, Grigio Calo, Blu Italia)
    "#1f77b4", "#7f7f7f", "#1f77b4",
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
    
    # Transizione Centrale
    "rgba(150, 150, 150, 0.5)", # Calo Import
    "rgba(31, 119, 180, 0.3)",  # Passaggio da 2020 a 2025
    
    # Uscite verso 2025
    "rgba(214, 39, 40, 0.4)",   
    "rgba(44, 160, 44, 0.4)",   
    "rgba(148, 103, 189, 0.4)", 
    "rgba(227, 119, 194, 0.4)", 
    "rgba(140, 86, 75, 0.4)",   
    "rgba(23, 190, 207, 0.4)"   
]

# ----------------------------------------------------
# 4. Creazione Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node = dict(
      pad = 20,
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

st.plotly_chart(fig, use_container_width=True)
"""

with open(file_path, "w") as f:
    f.write(code)

print(f"File generato con successo: {file_path}")
