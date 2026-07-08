import plotly.graph_objects as go
import pandas as pd

# Data structure based on user request (direct country-to-country flow in percentages)

# Values in Gmc (BCM - Billion Cubic Meters)
import_2020 = {
    "Russia": 28.4,
    "Algeria": 12.1,
    "GNL (Navi)": 13.1,
    "Nord Europa": 7.5,
    "Libia": 4.4,
    "Azerbaigian (TAP)": 0.0
}

import_2025 = {
    "Russia": 0.8,
    "Algeria": 20.1,
    "GNL (Navi)": 20.9,
    "Nord Europa": 8.6,
    "Libia": 0.9,
    "Azerbaigian (TAP)": 10.0
}

tot_2020 = sum(import_2020.values())
tot_2025 = sum(import_2025.values())

print(f"Total 2020: {tot_2020:.1f} BCM")
print(f"Total 2025: {tot_2025:.1f} BCM")

# Calculating percentages
perc_2020 = {k: (v/tot_2020)*100 for k, v in import_2020.items()}
perc_2025 = {k: (v/tot_2025)*100 for k, v in import_2025.items()}

for k in perc_2020.keys():
    print(f"{k}: 2020 -> {perc_2020[k]:.1f}% | 2025 -> {perc_2025[k]:.1f}%")
