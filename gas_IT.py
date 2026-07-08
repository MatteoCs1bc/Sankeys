import streamlit as st
import plotly.graph_objects as go

# ----------------------------------------------------
# 1. Configurazione della pagina Streamlit (Opzionale)
# ----------------------------------------------------
st.set_page_config(page_title="Flussi Gas Italia", layout="wide")

st.title("Diagramma Flussi Gas Italia")

# ----------------------------------------------------
# 2. Il tuo codice Plotly
# ----------------------------------------------------
# Definizione dei nodi del grafico
label = [
    "Import 2020", "Import 2025",                  # 0, 1 (Sorgenti)
    "Russia", "Algeria", "GNL (Via Nave)",          # 2, 3, 4 (Intermedi)
    "Nord Europa", "Libia", "Azerbaigian (TAP)",    # 5, 6, 7 (Intermedi)
    "Italia Totale 2020", "Italia Totale 2025"      # 8, 9 (Destinazioni)
]

# Definizione dei flussi (Sorgente -> Destinazione -> Valore)
source = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 7]
target = [2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9]
value =  [28.4, 12.1, 13.1, 7.5, 4.4, 0.8, 20.1, 20.9, 8.6, 0.9, 10.0, 28.4, 12.1, 13.1, 7.5, 4.4, 0.8, 20.1, 20.9, 8.6, 0.9, 10.0]

# Creazione del grafico Sankey
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = label,
      color = "blue"
    ),
    link = dict(
      source = source,
      target = target,
      value = value
  ))])

fig.update_layout(title_text="Variazione Flussi Gas Italia: 2020 vs 2025 (Gmc)", font_size=12)

# ----------------------------------------------------
# 3. Il comando MAGICO per Streamlit
# ----------------------------------------------------
st.plotly_chart(fig, use_container_width=True)
