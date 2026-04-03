import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Sankey Bilancio Energetico", layout="wide")

st.title("📊 Generatore Diagramma di Sankey: Bilancio Energetico")

# ---------------------------------------------------------
# 1. INPUT UTENTE NELLA SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("Configurazione")
nome_comune = st.sidebar.text_input("Nome del Comune", value="COMUNE GENERICO")
uploaded_file = st.sidebar.file_uploader("Carica l'Excel dei consumi", type=["xlsx"])

# ---------------------------------------------------------
# 2. CARICAMENTO DATI
# ---------------------------------------------------------
data_str = """VETTORE	Edifici comunali	IP	Residenz	Terz	Industr	Agric	Trasp	Parco auto	Trasporto pubblico	Autoprodotto
EN ELETTRICA	317.6	809.1	8625.7	7575.9	1802.1	3042.8	0	0	0	0
METANO	1750.0	0	33126.7	16932.6	4755.8	0	255.8	0	0	0
BENZINA	0	0	0	0	0	0	24325.6	17.4	0	0
GASOLIO	0	0	3019.8	440.7	0	0	32058.1	130.2	0	0
GPL	0	0	1484.9	0	0	0	1476.7	0	0	0
BIOMASSE	0	0	22243.0	0	0	0	0	0	0	0
RIFIUTI	0	0	0	0	0	0	0	0	0	0
IDRO	0	0	0	0	0	0	0	0	0	0
PV	0	0	0	0	0	0	0	0	0	20"""

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=0)
    st.sidebar.success("File caricato con successo!")
else:
    st.sidebar.info("Utilizzo dati di esempio. Carica un file per personalizzare.")
    df = pd.read_csv(io.StringIO(data_str), sep='\t', decimal='.', index_col=0)

# Pulizia dati
df = df.fillna(0)
df = df / 1000 # Conversione in MWh

# ---------------------------------------------------------
# 3. MAPPATURA NOMI E COLORI (Invariati dal tuo logico)
# ---------------------------------------------------------
rename_dict = {
    "Edifici comunali": "Edifici comunali", "IP": "Illuminazione Pubblica",
    "Residenz": "Residenziale", "Terz": "Terziario", "Industr": "Industria",
    "Agric": "Agricoltura", "Trasp": "Trasporto", "Parco auto": "Parco auto comunale",
    "Trasporto pubblico": "Trasporto pubblico", "Autoprodotto": "Autoprodotto"
}
df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns}, inplace=True)

# [Qui inseriresti tutte le tue definizioni di colori C_NODE_... e L_... come nel tuo script originale]
# Per brevità le ho raggruppate, ma nel tuo file tieni le tue definizioni.
C_NODE_ENELETTRICA = "rgba(255, 215, 0, 1)"
C_NODE_SETTORI = "rgba(176, 224, 230, 1)"
L_ELETTRICITA = "rgba(255, 215, 0, 0.5)"
L_PERDITE = "rgba(255, 0, 0, 0.8)"
L_FOSSILI_TO_EL = "rgba(0, 0, 0, 1)"
L_RINNOV_TO_EL = "rgba(0, 255, 0, 0.6)"
L_RESTO_TO_EL = "rgba(147, 112, 219, 0.5)"
L_TRASPORTI = "rgba(64, 64, 64, 0.7)"
L_CALORE = "rgba(139, 0, 0, 0.6)"

mix_pct = {
    "Combustibili gassosi (gas naturale, GNL, GPL)": 38.88,
    "Petrolio (Benzina, Gasolio)": 2.74,
    "Carbone": 1.50,
    "Biocombustibili": 4.75,
    "Rifiuti": 1.54,
    "Idroelettrico": 17.37,
    "Solare fotovoltaico": 11.53,
    "Eolico": 7.14,
    "Altro": 2.06,
    "Import": 12.49
}

# ---------------------------------------------------------
# 4. LOGICA SANKEY (Core del tuo codice)
# ---------------------------------------------------------
consumo_el_tot = df.loc["EN ELETTRICA"].sum() if "EN ELETTRICA" in df.index else df.iloc[0].sum()
pv_local_val = df.loc["PV", "Autoprodotto"] if ("PV" in df.index and "Autoprodotto" in df.columns) else 0
idro_local_val = df.loc["IDRO", "Autoprodotto"] if ("IDRO" in df.index and "Autoprodotto" in df.columns) else 0
tot_autoprodotto = pv_local_val + idro_local_val

# Etichette e Nodi
lbl_en_el = "Energia Elettrica"
lbl_perdite = "Perdite termiche di conversione"
nodi_L1 = [
    "Idroelettrico", "Eolico", "Solare fotovoltaico", "Import", 
    "Biocombustibili", "Rifiuti", "Carbone", "Altro",
    f"Solare autoprodotto ({nome_comune})", f"Idroelettrico autoprodotto ({nome_comune})",
    "Biomasse legnose", "Combustibili gassosi (gas naturale, GNL, GPL)", "Petrolio (Benzina, Gasolio)"
]

labels = nodi_L1 + [lbl_en_el, lbl_perdite]
settori = [c for c in df.columns if c != "Autoprodotto"]
labels += settori

idx_map = {name: i for i, name in enumerate(labels)}

sources, targets, values, link_colors = [], [], [], []

# Calcolo Rete
fabbisogno_rete = max(0, consumo_el_tot - tot_autoprodotto)
en_primaria = fabbisogno_rete * 2.42
perdite_val = en_primaria - fabbisogno_rete

# Flussi Mix -> Elettrico
for key_mix, pct in mix_pct.items():
    val = (en_primaria * pct) / 100
    if val > 0:
        # Mappatura semplificata per brevità
        src_name = next((n for n in nodi_L1 if n.startswith(key_mix[:5])), None)
        if src_name:
            sources.append(idx_map[src_name])
            targets.append(idx_map[lbl_en_el])
            values.append(val)
            link_colors.append(L_FOSSILI_TO_EL if "Petrolio" in key_mix or "gassosi" in key_mix else L_RINNOV_TO_EL)

# Elettrico -> Perdite e Settori
sources.append(idx_map[lbl_en_el]); targets.append(idx_map[lbl_perdite]); values.append(perdite_val); link_colors.append(L_PERDITE)

for s in settori:
    val_el = df.loc["EN ELETTRICA", s] if "EN ELETTRICA" in df.index else 0
    if val_el > 0:
        sources.append(idx_map[lbl_en_el]); targets.append(idx_map[s]); values.append(val_el); link_colors.append(L_ELETTRICITA)

# Termico / Trasporti
map_termico = {"METANO": nodi_L1[11], "GPL": nodi_L1[11], "GASOLIO": nodi_L1[12], "BENZINA": nodi_L1[12], "BIOMASSE": nodi_L1[10]}
for inp, t_L1 in map_termico.items():
    if inp in df.index:
        for s in settori:
            val = df.loc[inp, s]
            if val > 0:
                sources.append(idx_map[t_L1]); targets.append(idx_map[s]); values.append(val)
                link_colors.append(L_TRASPORTI if "Trasp" in s or "auto" in s else L_CALORE)

# ---------------------------------------------------------
# 5. RENDER GRAFICO
# ---------------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    valueformat=".1f", valuesuffix=" MWh",
    node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels),
    link=dict(source=sources, target=targets, value=values, color=link_colors)
)])

fig.update_layout(title_text=f"Bilancio Energetico {nome_comune}", font_size=12, height=800)

# Invece di scrivere l'HTML, lo mostriamo in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Tabella dati per controllo
with st.expander("Visualizza Tabella Dati Originale"):
    st.dataframe(df * 1000) # Riportiamo in unità originali per la tabella
