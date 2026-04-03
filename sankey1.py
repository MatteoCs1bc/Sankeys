import pandas as pd
import io
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. INPUT UTENTE (Nome Comune)
# ---------------------------------------------------------
# NOME_COMUNE = "COMUNE GENERICO"
NOME_COMUNE = input("Inserisci il nome del Comune: ")

print(f"Elaborazione dati per: {NOME_COMUNE}...")

# ---------------------------------------------------------
# 2. CARICAMENTO DATI
# ---------------------------------------------------------
# Dati di fallback per test (nel caso manchi il file Excel)
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

# Lettura del file
try:
    df = pd.read_excel('dati_input.xlsx', index_col=0)
except FileNotFoundError:
    print("ATTENZIONE: File 'dati_input.xlsx' non trovato. Utilizzo i dati di esempio interni.")
    df = pd.read_csv(io.StringIO(data_str), sep='\t', decimal='.', index_col=0)

# Pulizia dati: Riempie celle vuote con 0 e converte in MWh
df = df.fillna(0)
df = df / 1000

# ---------------------------------------------------------
# 3. MAPPATURA NOMI
# ---------------------------------------------------------
rename_dict = {
    "Edifici comunali": "Edifici comunali", "IP": "Illuminazione Pubblica",
    "Residenz": "Residenziale", "Terz": "Terziario", "Industr": "Industria",
    "Agric": "Agricoltura", "Trasp": "Trasporto", "Parco auto": "Parco auto comunale",
    "Trasporto pubblico": "Trasporto pubblico", "Autoprodotto": "Autoprodotto"
}
cols_found = {k: v for k, v in rename_dict.items() if k in df.columns}
df.rename(columns=cols_found, inplace=True)

# ---------------------------------------------------------
# 4. COLORI E PARAMETRI
# ---------------------------------------------------------
# Colori Nodi
C_NODE_FOSSILI = "rgba(64, 64, 64, 1)"  # Grigio Scuro
C_NODE_RINNOV = "rgba(0, 200, 0, 1)"  # Verde
C_NODE_GAS = "rgba(211, 211, 211, 1)"  # Grigio Chiaro
C_NODE_PETROLIO = "rgba(64, 64, 64, 1)"  # Grigio Scuro
C_NODE_BIOCOMB = "rgba(255, 165, 0, 1)"  # Arancione
C_NODE_CARBONE = "rgba(0, 0, 0, 1)"  # Nero
C_NODE_IMPORT = "rgba(75, 0, 130, 1)"  # Viola
C_NODE_PV = "rgba(255, 215, 0, 1)"  # Giallo
C_NODE_PV_AUTO = "rgba(255, 140, 0, 1)"  # Arancione Caldo
C_NODE_IDRO = "rgba(0, 0, 255, 1)"  # Blu
C_NODE_IDRO_AUTO = "rgba(0, 191, 255, 1)"  # DeepSkyBlue
C_NODE_ENELETTRICA = "rgba(255, 215, 0, 1)"  # Giallo
C_NODE_PERDITE = "rgba(255, 0, 0, 1)"  # Rosso Acceso
C_NODE_SETTORI = "rgba(176, 224, 230, 1)"  # Powder Blue

# Colori Flussi
L_FOSSILI_TO_EL = "rgba(0, 0, 0, 1)"  # Nero Totale
L_RINNOV_TO_EL = "rgba(0, 255, 0, 0.6)"  # Verde Acceso
L_RESTO_TO_EL = "rgba(147, 112, 219, 0.5)"  # Viola
L_ELETTRICITA = "rgba(255, 215, 0, 0.5)"  # Giallo
L_CALORE = "rgba(139, 0, 0, 0.6)"  # Rosso Scuro
L_TRASPORTI = "rgba(64, 64, 64, 0.7)"  # Grigio Scuro
L_PERDITE = "rgba(255, 0, 0, 0.8)"  # Rosso Acceso

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
# 5. CREAZIONE NODI E ORDINAMENTO
# ---------------------------------------------------------
try:
    consumo_el_tot = df.loc["EN ELETTRICA"].sum()
except KeyError:
    consumo_el_tot = df.iloc[0].sum()

# Lettura Autoproduzione PV
pv_local_val = 0
if "PV" in df.index and "Autoprodotto" in df.columns:
    pv_local_val = df.loc["PV", "Autoprodotto"]

# Lettura Autoproduzione IDRO (Nuovo)
idro_local_val = 0
if "IDRO" in df.index and "Autoprodotto" in df.columns:
    idro_local_val = df.loc["IDRO", "Autoprodotto"]

tot_autoprodotto = pv_local_val + idro_local_val

pct_pv_auto = 0
pct_idro_auto = 0
if consumo_el_tot > 0:
    pct_pv_auto = (pv_local_val / consumo_el_tot) * 100
    pct_idro_auto = (idro_local_val / consumo_el_tot) * 100

# Etichette
lbl_gas = "Combustibili gassosi (gas naturale, GNL, GPL)"
lbl_petrolio = "Petrolio (Benzina, Gasolio)"
lbl_carbone = "Carbone"
lbl_biocomb = "Biocombustibili"
lbl_rifiuti = "Rifiuti"
lbl_idro = "Idroelettrico"
lbl_pv_mix = "Solare fotovoltaico"
lbl_pv_auto = f"Solare autoprodotto ({NOME_COMUNE}) [{pct_pv_auto:.1f}%]"
lbl_idro_auto = f"Idroelettrico autoprodotto ({NOME_COMUNE}) [{pct_idro_auto:.1f}%]"
lbl_eolico = "Eolico"
lbl_biomasse = "Biomasse legnose"
lbl_altro = "Altro"
lbl_import = "Import"
lbl_en_el = "Energia Elettrica"
lbl_perdite = "Perdite termiche di conversione"

# --- ORDINAMENTO NODI SX (Come richiesto fissato) ---
nodi_L1 = [
    # -- 1. Mix Elettrico da Rete --
    lbl_idro,
    lbl_eolico,
    lbl_pv_mix,
    lbl_import,
    lbl_biocomb,
    lbl_rifiuti,
    lbl_carbone,
    lbl_altro,

    # -- 2. Autoproduzione --
    lbl_pv_auto,
    lbl_idro_auto,

    # -- 3. Resto Combustibili (Biomasse -> Gas -> Petrolio) --
    lbl_biomasse,
    lbl_gas,
    lbl_petrolio
]

map_colori = {
    lbl_gas: C_NODE_GAS, lbl_petrolio: C_NODE_PETROLIO, lbl_carbone: C_NODE_CARBONE,
    lbl_biocomb: C_NODE_BIOCOMB, lbl_rifiuti: C_NODE_RINNOV, lbl_idro: C_NODE_IDRO,
    lbl_pv_mix: C_NODE_PV, lbl_pv_auto: C_NODE_PV_AUTO, lbl_eolico: "skyblue",
    lbl_biomasse: "saddlebrown", lbl_altro: "teal", lbl_import: C_NODE_IMPORT,
    lbl_idro_auto: C_NODE_IDRO_AUTO
}

labels = nodi_L1 + [lbl_en_el, lbl_perdite]
idx_map = {name: i for i, name in enumerate(labels)}
current_idx = len(labels)

settori = [c for c in df.columns if c != "Autoprodotto"]
idx_settori = {}
for s in settori:
    idx_settori[s] = current_idx
    labels.append(s)
    current_idx += 1

node_colors = []
for lbl in labels:
    if lbl in map_colori:
        node_colors.append(map_colori[lbl])
    elif lbl == lbl_en_el:
        node_colors.append(C_NODE_ENELETTRICA)
    elif lbl == lbl_perdite:
        node_colors.append(C_NODE_PERDITE)
    else:
        node_colors.append(C_NODE_SETTORI)

# ---------------------------------------------------------
# 6. GENERAZIONE FLUSSI
# ---------------------------------------------------------
sources = []
targets = []
values = []
link_colors = []

# ELETTRICO
# Il netto da rete sottrae TUTTA l'autoproduzione (PV + Idro)
fabbisogno_rete = max(0, consumo_el_tot - tot_autoprodotto)
en_primaria = fabbisogno_rete * 2.42
perdite_val = en_primaria - fabbisogno_rete

# 1. Mix -> Elettrico
for key_mix, pct in mix_pct.items():
    val = (en_primaria * pct) / 100
    if val > 0:
        t_name = None
        if "gassosi" in key_mix:
            t_name = lbl_gas
        elif "Petrolio" in key_mix:
            t_name = lbl_petrolio
        elif "Carbone" in key_mix:
            t_name = lbl_carbone
        elif "Biocomb" in key_mix:
            t_name = lbl_biocomb
        elif "Rifiuti" in key_mix:
            t_name = lbl_rifiuti
        elif "Idro" in key_mix:
            t_name = lbl_idro
        elif "Solare" in key_mix:
            t_name = lbl_pv_mix
        elif "Eolico" in key_mix:
            t_name = lbl_eolico
        elif "Altro" in key_mix:
            t_name = lbl_altro
        elif "Import" in key_mix:
            t_name = lbl_import

        if t_name:
            sources.append(idx_map[t_name])
            targets.append(idx_map[lbl_en_el])
            values.append(val)
            if t_name in [lbl_gas, lbl_petrolio, lbl_carbone]:
                link_colors.append(L_FOSSILI_TO_EL)
            elif t_name in [lbl_idro, lbl_pv_mix, lbl_eolico, lbl_biomasse]:
                link_colors.append(L_RINNOV_TO_EL)
            else:
                link_colors.append(L_RESTO_TO_EL)

# 2. PV Auto -> Elettrico
if pv_local_val > 0:
    sources.append(idx_map[lbl_pv_auto])
    targets.append(idx_map[lbl_en_el])
    values.append(pv_local_val)
    link_colors.append(L_RINNOV_TO_EL)

# 3. Idro Auto -> Elettrico
if idro_local_val > 0:
    sources.append(idx_map[lbl_idro_auto])
    targets.append(idx_map[lbl_en_el])
    values.append(idro_local_val)
    link_colors.append(L_RINNOV_TO_EL)

# 4. Elettrico -> Perdite
if perdite_val > 0:
    sources.append(idx_map[lbl_en_el])
    targets.append(idx_map[lbl_perdite])
    values.append(perdite_val)
    link_colors.append(L_PERDITE)

# 5. Elettrico -> Settori
for s in settori:
    val = df.loc["EN ELETTRICA", s]
    if val > 0:
        sources.append(idx_map[lbl_en_el])
        targets.append(idx_settori[s])
        values.append(val)
        link_colors.append(L_ELETTRICITA)

# TERMICO / TRASPORTI
map_L1_dir = {"METANO": lbl_gas, "GPL": lbl_gas, "GASOLIO": lbl_petrolio, "BENZINA": lbl_petrolio,
              "BIOMASSE": lbl_biomasse}
for inp, t_L1 in map_L1_dir.items():
    if inp in df.index:
        for s in settori:
            val = df.loc[inp, s]
            if val > 0:
                sources.append(idx_map[t_L1])
                targets.append(idx_settori[s])
                values.append(val)
                if s in ["Trasporto", "Parco auto comunale", "Trasporto pubblico"]:
                    link_colors.append(L_TRASPORTI)
                else:
                    link_colors.append(L_CALORE)

# ---------------------------------------------------------
# 7. OUTPUT
# ---------------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    valueformat=".1f", valuesuffix=" MWh",
    node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels, color=node_colors),
    link=dict(source=sources, target=targets, value=values, color=link_colors)
)])

fig.update_layout(title_text=f"<b>Bilancio Energetico {NOME_COMUNE}</b><br>Analisi Flussi (MWh)", font_size=12,
                  template="plotly_white", width=1600, height=900)
nome_file = f"sankey_{NOME_COMUNE.replace(' ', '_')}.html"
fig.write_html(nome_file, auto_open=True)
print(f"File generato: {nome_file}")
