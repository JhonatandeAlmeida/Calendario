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

logo = config.get(
    "Logo",
    "logo.png"
)

mes_atual = config.get(
    "MesAtual",
    "Setembro"
)

regional_padrao = config.get(
    "RegionalPadrao",
    "AM"
)

# ==================================================
# FILTROS
# ==================================================

meses = sorted(
    prod_df["Mes"].unique()
)

regionais = sorted(
    prod_df["Regional"].unique()
)

mes_index = (
    meses.index(mes_atual)
    if mes_atual in meses
    else 0
)

regional_index = (
    regionais.index(regional_padrao)
    if regional_padrao in regionais
    else 0
)

col_f1, col_f2 = st.columns(2)

with col_f1:
    mes = st.selectbox(
        "Mês",
        meses,
        index=mes_index
    )

with col_f2:
    regional = st.selectbox(
        "Regional",
        regionais,
        index=regional_index
    )

# ==================================================
# FILTRAGEM
# ==================================================

produtos = prod_df[
    (prod_df["Mes"] == mes)
    &
    (prod_df["Regional"] == regional)
]

mecanica = mec_df[
    mec_df["Regional"] == regional
]

# ==================================================
# CALENDÁRIO
# ==================================================

cal_df["Data"] = pd.to_datetime(
    cal_df["Data"]
)

mes_numero = {
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
}.get(mes)

ano = int(config.get("AnoAtual", 2026))

cal_mes = cal_df[
    (cal_df["Data"].dt.month == mes_numero)
    &
    (cal_df["Data"].dt.year == ano)
]

eventos = {}

for _, row in cal_mes.iterrows():
    eventos[row["Data"].day] = row["Tipo"]

# ==================================================
# CABEÇALHO
# ==================================================

col_title, col_logo = st.columns([8, 1])

with col_title:

    st.markdown(
        f"""
        <div class='main-title'>
            {titulo.upper()} | {mes.upper()} - {ano}
        </div>
        """,
        unsafe_allow_html=True
    )

with col_logo:

    try:
        st.image(
            f"images/{logo}",
            width=100
        )
    except:
        pass

# ==================================================
# CALENDÁRIO + MECÂNICA
# ==================================================

col1, col2 = st.columns(
    [1.05, 1.25]
)

with col1:

    st.markdown(
        "<div class='section-title'>Calendário</div>",
        unsafe_allow_html=True
    )

    gerar_calendario(
        ano,
        mes_numero,
        eventos
    )

with col2:

    st.markdown(
        "<div class='section-title'>Mecânica</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='mecanica-box'>",
        unsafe_allow_html=True
    )

    for _, row in mecanica.iterrows():
        st.markdown(
            f"• {row['Texto']}"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# ==================================================
# CARDS PRODUTOS
# ==================================================

def mostrar_canal(df, canal):

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='canal-title'>
            {canal}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(8)

    for i, (_, row) in enumerate(df.iterrows()):

        with cols[i % 8]:

            try:
                st.image(
                    f"images/produtos/{row['Imagem']}",
                    use_container_width=True
                )
            except:
                st.empty()

            st.markdown(
                f"""
                <div class='sku-name'>
                    {row['SKU']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class='old-price'>
                    R$ {row['De']:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class='new-price'>
                    R$ {row['Para']:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

# ==================================================
# CANAIS DINÂMICOS
# ==================================================

for canal in produtos["Canal"].unique():

    df_canal = produtos[
        produtos["Canal"] == canal
    ]

    mostrar_canal(
        df_canal,
        canal
    )
