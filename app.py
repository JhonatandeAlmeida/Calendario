import streamlit as st
import pandas as pd

from components.calendar import gerar_calendario
from components.styles import load_css

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
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

try:

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

except Exception as e:

    st.error(f"Erro ao ler planilha: {e}")
    st.stop()

# ==================================================
# CONFIG
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

mes_atual = config.get(
    "MesAtual",
    "Setembro"
)

regional_padrao = config.get(
    "RegionalPadrao",
    "AM"
)

ano = int(
    config.get(
        "AnoAtual",
        2026
    )
)

logo = config.get(
    "Logo",
    "logo.png"
)

# ==================================================
# FILTROS
# ==================================================

meses = sorted(
    prod_df["Mes"]
    .dropna()
    .astype(str)
    .unique()
)

regionais = sorted(
    prod_df["Regional"]
    .dropna()
    .astype(str)
    .unique()
)

if not meses:
    st.error("Nenhum mês encontrado.")
    st.stop()

if not regionais:
    st.error("Nenhuma regional encontrada.")
    st.stop()

col_f1, col_f2 = st.columns(2)

with col_f1:

    mes = st.selectbox(
        "Mês",
        meses,
        index=meses.index(mes_atual)
        if mes_atual in meses else 0
    )

with col_f2:

    regional = st.selectbox(
        "Regional",
        regionais,
        index=regionais.index(regional_padrao)
        if regional_padrao in regionais else 0
    )

# ==================================================
# FILTROS DOS PRODUTOS
# ==================================================

produtos = prod_df[
    (prod_df["Mes"].astype(str) == mes)
    &
    (prod_df["Regional"].astype(str) == regional)
]

mecanica = mec_df[
    mec_df["Regional"].astype(str) == regional
]

# ==================================================
# CALENDÁRIO
# ==================================================

cal_df["Data"] = pd.to_datetime(
    cal_df["Data"]
)

mapa_meses = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12
}

mes_numero = mapa_meses.get(
    mes,
    9
)

cal_mes = cal_df[
    (cal_df["Data"].dt.month == mes_numero)
    &
    (cal_df["Data"].dt.year == ano)
]

eventos = {}

for _, row in cal_mes.iterrows():

    eventos[
        row["Data"].day
    ] = row["Tipo"]

# ==================================================
# TÍTULO
# ==================================================

col_titulo, col_logo = st.columns([8, 1])

with col_titulo:

    st.markdown(
        f"""
        <div class='main-title'>
        {titulo} | {mes} {ano}
        </div>
        """,
        unsafe_allow_html=True
    )

with col_logo:

    try:

        st.image(
            f"images/{logo}",
            width=120
        )

    except:
        pass

# ==================================================
# CALENDÁRIO / MECÂNICA
# ==================================================

col1, col2 = st.columns([1, 1])

with col1:

    st.markdown(
        """
        <div class='section
