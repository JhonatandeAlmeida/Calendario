import streamlit as st
import pandas as pd

from components.calendar import gerar_calendario
from components.styles import load_css

# ==================================================
# CONFIGURAÇÃO
# ==================================================

st.set_page_config(
    page_title="Calendário Promocional",
    page_icon="📅",
    layout="wide"
)

load_css()

# ==================================================
# LEITURA DO EXCEL
# ==================================================

ARQUIVO = "data/calendario_promocional.xlsx"

config_df = pd.read_excel(
    ARQUIVO,
    sheet_name="CONFIG"
)

cal_df = pd.read_excel(
    ARQUIVO,
    sheet_name="CALENDARIO"
)

mec_df = pd.read_excel(
    ARQUIVO,
    sheet_name="MECANICA"
)

prod_df = pd.read_excel(
    ARQUIVO,
    sheet_name="PRODUTOS"
)

# ==================================================
# CONFIGURAÇÕES
# ==================================================

config = dict(
    zip(
        config_df["Chave"],
        config_df["Valor"]
    )
)

titulo = config.get(
    "Titulo",
    "Calendário Promocional"
)

logo = 
