import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Flussi Gas Italia", layout="wide")
st.title("Evoluzione dell'approvvigionamento di Gas in Italia (2020 vs 2025)")
st.markdown("Valori in **Miliardi di metri cubi (Gmc)** e peso percentuale. Nodi ordinati per volume importato.")

# ----------------------------------------------------
# 1. Definizione delle etichette (Nodi) ordinate per volume decrescente
# ----------------------------------------------------
label = [
    # Nodi 2020 (0-4) - Ordine: Russia, GNL, Algeria, Nord Europa, Libia
    "Russia (28.4 Gmc | 43.4%)",                  # 0
    "GNL (USA, Qatar, Algeria) (13.1 Gmc | 20.0%)", # 1
    "Algeria (12.1 Gmc | 18.5%)",                 # 2
    "Nord Europa (7.5 Gmc | 11.5%)",              # 3
    "Libia (4.4 Gmc | 6.7%)",                     # 4
    
    # Nodi Centrali (5, 6)
    "Sistema Gas Italia",                         # 5
    "Calo Import (-4.2 Gmc)",                     # 6
    
    # Nodi 2025 (7-12) - Ordine: GNL, Algeria, Azerbaigian, Nord Europa, Libia, Russia
    "GNL (USA, Qatar, Algeria) (20.9 Gmc | 34.1%)", # 7
    "Algeria (20.1 Gmc | 32.8%)",                 # 8
    "Azerbaigian (10.0 Gmc | 16.3%)",             # 9
    "Nord Europa (8.6 Gmc | 14.0%)",              # 10
    "Libia (0.9 Gmc | 1.5%)",                     # 11
    "Russia (0.8 Gmc | 1.3%)"                     # 12
]

# ----------------------------------------------------
# 2. Forzatura delle Coordinate (X e Y)
# ----------------------------------------------------
# Spaziatura dinamica approssimativa basata sui volumi
x_pos = [
    0.01, 0.01, 0.01, 0.01, 0.01,  # 0-4: Sinistra (2020)
    0.5,                           # 5: Sistema Italia
    0.5,                           # 6: Calo Import
    0.99, 0.99, 0.99, 0.99, 0.99, 0.99 # 7-12: Destra (2025)
]

y_pos = [
    # 2020 (dall'alto al basso)
    0.15,  # Russia
    0.45,  # GNL
    0.65,  # Algeria
    0.85,  # Nord Europa
    0.98,  # Libia
    
    0.01,  # 5: Sistema Italia in alto
    0.99,  # 6: Calo Import in basso
    
    # 2025 (dall'alto al basso)
    0.15,  # GNL
    0.40,  # Algeria
    0.65,  # Azerbaigian
    0.80,  # Nord Europa
    0.90,  # Libia
    0.98   # Russia
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
    28.4, 13.1, 12.1, 7.5, 4.4, # Volumi in ingresso 2020 (ordinati come nodi 0-4)
    4.2,                        # Volume del calo
    20.9, 20.1, 10.0, 8.6, 0.9, 0.8 # Volumi in uscita verso il mix 2025 (ordinati come nodi 7-12)
]

# ----------------------------------------------------
# 4. Colori - MANTENUTI E RIORDINATI
# ----------------------------------------------------
color_map = {
    "Russia": "#d62728",      # Rosso
    "Algeria": "#2ca02c",     # Verde
    "GNL": "#9467bd",         # Viola
    "Nord Europa": "#e377c2", # Rosa
    "Libia": "#8c564b",       # Marrone
    "Azerbaigian": "#17becf", # Ciano
    "Italia": "#1f77b4",      # Blu
    "Calo": "#7f7f7f"         # Grigio
}

node_colors = [
    # Colori 2020
    color_map["Russia"], color_map["GNL"], color_map["Algeria"], color_map["Nord Europa"], color_map["Libia"],
    # Colori Centrali
    color_map["Italia"], color_map["Calo"],
    # Colori 2025
    color_map["GNL"], color_map["Algeria"], color_map["Azerbaigian"], color_map["Nord Europa"], color_map["Libia"], color_map["Russia"]
]

link_colors = [
    # Ingressi 2020 (colorati con alpha 0.4)
    "rgba(214, 39, 40, 0.4)",   # Russia
    "rgba(148, 103, 189, 0.4)", # GNL
    "rgba(44, 160, 44, 0.4)",   # Algeria
    "rgba(227, 119, 194, 0.4)", # Nord Europa
    "rgba(140, 86, 75, 0.4)",   # Libia
    
    # Uscite verso Calo
    "rgba(150, 150, 150, 0.5)",
    
    # Uscite verso 2025
    "rgba(148, 103, 189, 0.4)", # GNL
    "rgba(44, 160, 44, 0.4)",   # Algeria
    "rgba(23, 190, 207, 0.4)",  # Azerbaigian
    "rgba(227, 119, 194, 0.4)", # Nord Europa
    "rgba(140, 86, 75, 0.4)",   # Libia
    "rgba(214, 39, 40, 0.4)"    # Russia
]

# ----------------------------------------------------
# 5. Creazione Grafico
# ----------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="freeform", 
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
