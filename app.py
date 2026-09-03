import streamlit as st
import pandas as pd

from components.calendar import gerar_calendario
from components.styles import load_css

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================

st.set_page_config(
    page_title="Calendário Promocional",
    page_icon="📅",
    layout="wide"
)

load_css()

# ======================================================
# LEITURA DO ARQUIVO EXCEL
# ======================================================

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

# ======================================================
# CONFIGURAÇÕES
# ======================================================

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

ano = int(
    config.get(
        "AnoAtual",
        2026
    )
)

# ======================================================
# FILTROS
# ======================================================

meses = sorted(
    prod_df["Mes"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

regionais = sorted(
    prod_df["Regional"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
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

# ======================================================
# FILTRAGEM DOS DADOS
# ======================================================

produtos = prod_df[
    (prod_df["Mes"].astype(str) == mes) &
    (prod_df["Regional"].astype(str) == regional)
]

mecanica = mec_df[
    mec_df["Regional"].astype(str) == regional
]

# ======================================================
# CALENDÁRIO
# ======================================================

cal_df["Data"] = pd.to_datetime(
    cal_df["Data"]
)

meses_numericos = {
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

mes_numero = meses_numericos.get(mes)

cal_mes = cal_df[
    (cal_df["Data"].dt.month == mes_numero) &
    (cal_df["Data"].dt.year == ano)
]

eventos = {}

for _, row in cal_mes.iterrows():
    eventos[row["Data"].day] = row["Tipo"]

# ======================================================
# CABEÇALHO
# ======================================================

col_titulo, col_logo = st.columns([8, 1])

with col_titulo:

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
            width=120
        )
    except:
        pass

# ======================================================
# CALENDÁRIO E MECÂNICA
# ======================================================

col1, col2 = st.columns([1, 1])

with col1:

    st.markdown(
        """
        <div class='section-title'>
            Calendário
        </div>
        """,
        unsafe_allow_html=True
    )

    gerar_calendario(
        ano,
        mes_numero,
        eventos
    )

with col2:

    st.markdown(
        """
        <div class='section-title'>
            Mecânica
        </div>
        """,
        unsafe_allow_html=True
    )

    itens = ""

    for _, row in mecanica.iterrows():
        itens += f"<li>{row['Texto']}</li>"

    st.markdown(
        f"""
        <div class='mecanica-box'>
            <ul>
                {itens}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# PRODUTOS
# ======================================================

def mostrar_canal(df_canal, nome_canal):

    if len(df_canal) == 0:
        return

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='canal-title'>
            {nome_canal}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    colunas = st.columns(6)

    for i, (_, row) in enumerate(df_canal.iterrows()):

        with colunas[i % 6]:

            try:
                st.image(
                    f"images/produtos/{row['Imagem']}",
                    use_container_width=True
                )
            except:
                st.image(
                    "https://placehold.co/200x200?text=SKU",
                    use_container_width=True
                )

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
                    R$ {float(row['De']):.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class='new-price'>
                    R$ {float(row['Para']):.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

# ======================================================
# EXIBE TODOS OS CANAIS
# ======================================================

for canal in produtos["Canal"].dropna().unique():

    mostrar_canal(
        produtos[
            produtos["Canal"] == canal
        ],
        canal
    )
