import streamlit as st
import pandas as pd
from PIL import Image
import os

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
Image as PdfImage,
Table,
TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet

from components.calendar import gerar_calendario
from components.styles import load_css

def padronizar_imagem(caminho_imagem):

    img = Image.open(caminho_imagem).convert("RGBA")

    tamanho = 800

    canvas = Image.new(
        "RGBA",
        (tamanho, tamanho),
        (255, 255, 255, 0)
    )

    proporcao = min(
        tamanho / img.width,
        tamanho / img.height
    ) * 0.6
    
    nova_largura = int(img.width * proporcao)
    nova_altura = int(img.height * proporcao)

    img = img.resize(
        (nova_largura, nova_altura),
        Image.LANCZOS
    )

    pos_x = (tamanho - nova_largura) // 2
    pos_y = (tamanho - nova_altura) // 2

    canvas.paste(
        img,
        (pos_x, pos_y),
        img
    )

    return canvas

# ==================================================
# FUNÇÃO PDF
# ==================================================

def gerar_pdf(
    titulo,
    mes,
    ano,
    mecanica_mes,
    produtos,
    logo
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elementos = []

    # Título

    elementos.append(
        Paragraph(
            f"<b>{titulo} | {mes} {ano}</b>",
            styles["Title"]
        )
    )

    elementos.append(Spacer(1, 10))

    # Logo

    try:

        elementos.append(
            Image(
                f"images/{logo}",
                width=3*cm,
                height=3*cm
            )
        )

    except:
        pass

    elementos.append(Spacer(1, 10))

    # Mecânica

    elementos.append(
        Paragraph(
            "<b>MECÂNICA</b>",
            styles["Heading2"]
        )
    )

    sell_in = mecanica_mes[
        mecanica_mes["Tipo"].str.upper()
        == "SELL IN"
    ]

    sell_out = mecanica_mes[
        mecanica_mes["Tipo"].str.upper()
        == "SELL OUT"
    ]

    elementos.append(
        Paragraph(
            "<b>SELL IN</b>",
            styles["Heading3"]
        )
    )

    for _, row in sell_in.iterrows():

        elementos.append(
            Paragraph(
                f"• {row['Texto']}",
                styles["BodyText"]
            )
        )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            "<b>SELL OUT</b>",
            styles["Heading3"]
        )
    )

    for _, row in sell_out.iterrows():

        elementos.append(
            Paragraph(
                f"• {row['Texto']}",
                styles["BodyText"]
            )
        )

    elementos.append(Spacer(1, 20))

    # Produtos

    for canal in produtos["Canal"].dropna().unique():

        elementos.append(
            Paragraph(
                f"<b>{canal}</b>",
                styles["Heading2"]
            )
        )

        df_canal = produtos[
            produtos["Canal"] == canal
        ]

        for quinzena in sorted(
            df_canal["Quinzena"].unique()
        ):

            elementos.append(
                Paragraph(
                    f"<b>{quinzena}ª QUINZENA</b>",
                    styles["Heading3"]
                )
            )

            dados = [
                [
                    "SKU",
                    "DE",
                    "PARA"
                ]
            ]

            produtos_q = df_canal[
                df_canal["Quinzena"] == quinzena
            ]

            for _, row in produtos_q.iterrows():

                dados.append(
                    [
                        str(row["SKU"]),
                        f"R$ {row['De']:.2f}",
                        f"R$ {row['Para']:.2f}"
                    ]
                )

            tabela = Table(
                dados,
                colWidths=[6*cm, 3*cm, 3*cm]
            )

            tabela.setStyle(
                TableStyle([
                    ("BACKGROUND", (0,0), (-1,0), colors.grey),
                    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                    ("GRID", (0,0), (-1,-1), 1, colors.black),
                    ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ])
            )

            elementos.append(tabela)
            elementos.append(Spacer(1, 10))

    doc.build(elementos)

    buffer.seek(0)

    return buffer
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
# PRODUTOS
# ==================================================

def mostrar_produtos(df_canal, canal, negocio):

    st.markdown(
        f"""
        <div class="canal-title">
            {canal}
        </div>
        """,
        unsafe_allow_html=True
    )

    quinzenas = sorted(
        df_canal["Quinzena"]
        .dropna()
        .unique()
    )
    max_skus = (
        df_canal.groupby("Quinzena")
        .size()
        .max()
    )

    for quinzena in quinzenas:

        st.markdown(
            f"""
            <div class="quinzena-title">
                {quinzena}ª QUINZENA
            </div>
            """,
            unsafe_allow_html=True
        )

        produtos_q = (
            df_canal[
                df_canal["Quinzena"] == quinzena
            ]
            .sort_values(
                by="Para",
                ascending=True
            )
        )

        qtd_skus = len(produtos_q)

        # Centraliza os produtos em relação à quinzena com mais SKUs
        offset = max((max_skus - qtd_skus) // 2, 0)
        
        cols = st.columns(max_skus)


        for i, (_, row) in enumerate(produtos_q.iterrows()):

            with cols[i + offset]:
                preco_de = float(row["De"])
                preco_para = float(row["Para"])

                delta_rs = preco_de - preco_para

                try:

                    st.image(
                        f"images/produtos_padronizados/{row['Imagem']}",
                        width=130
                    )

                except Exception:
                    st.empty()


                st.markdown(
                    f"""
                    <div class="sku-name">
                        {row['SKU']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="delta-price">
                        ↓ R$ {delta_rs:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="old-price">
                        R$ {preco_de:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="new-price">
                        R$ {preco_para:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<div style='height:20px'></div>",
                    unsafe_allow_html=True
                )
                                

# ==================================================
# LEITURA DA PLANILHA
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

    st.error(f"Erro ao abrir a planilha: {e}")
    st.stop()

# ==================================================
# PADRONIZAÇÃO DAS IMAGENS
# ==================================================

PASTA_ORIGINAL = "images/produtos"
PASTA_PADRONIZADA = "images/produtos_padronizados"

os.makedirs(
    PASTA_PADRONIZADA,
    exist_ok=True
)

for arquivo in os.listdir(PASTA_ORIGINAL):

    origem = os.path.join(
        PASTA_ORIGINAL,
        arquivo
    )

    destino = os.path.join(
        PASTA_PADRONIZADA,
        arquivo
    )

    try:

        imagem = padronizar_imagem(
            origem
        )

        imagem.save(
            destino,
            "PNG"
        )

    except Exception:
        pass

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

logo = config.get(
    "Logo",
    "logo.png"
)

ano = int(
    config.get(
        "AnoAtual",
        2026
    )
)

mes_padrao = config.get(
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
    prod_df["Mes"]
    .dropna()
    .astype(str)
    .unique()
)

negocios = sorted(
    prod_df["Tipo"]
    .dropna()
    .astype(str)
    .unique()
)

negocio = st.selectbox(
    "Tipo",
    negocios
)
regionais = sorted(
    prod_df.loc[
        prod_df["Tipo"] == negocio,
        "Regional"
    ]
    .dropna()
    .astype(str)
    .unique()
)

colf1, colf2 = st.columns(2)

with colf1:

    mes = st.selectbox(
        "Mês",
        meses,
        index=meses.index(mes_padrao)
        if mes_padrao in meses else 0
    )

with colf2:

    regional = st.selectbox(
        "Regional",
        regionais,
        index=regionais.index(regional_padrao)
        if regional_padrao in regionais else 0
    )
canais = sorted(
    prod_df.loc[
        (prod_df["Tipo"] == negocio)
        &
        (prod_df["Regional"] == regional),
        "Canal"
    ]
    .dropna()
    .astype(str)
    .unique()
)

canal = st.radio(
    "Canal",
    canais,
    horizontal=True
)
# ==================================================
# FILTROS DE DADOS
# ==================================================

produtos = prod_df[
    (prod_df["Tipo"].astype(str) == negocio)
    &
    (prod_df["Mes"].astype(str) == mes)
    &
    (prod_df["Regional"].astype(str) == regional)
    &
    (prod_df["Canal"].astype(str) == canal)
]
mecanica_mes = mec_df[
    (mec_df["SKU"].astype(str) == negocio)
    &
    (
        mec_df["Mes"]
        .astype(str)
        .str.strip()
        .str.upper()
        ==
        mes.strip().upper()
    )
]
# ==================================================
# CALENDÁRIO
# ==================================================

cal_df["Data"] = pd.to_datetime(
    cal_df["Data"]
)

meses_mapa = {
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

mes_numero = meses_mapa.get(
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
# CABEÇALHO
# ==================================================

col_title, col_logo = st.columns([8, 1])

with col_title:

    st.markdown(
        f"""
        <div class="main-title">
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
# CALENDÁRIO E MECÂNICA
# ==================================================

col_esquerda, col_direita = st.columns([0.8, 2.2])

with col_esquerda:

    st.markdown(
        """
        <div class="section-title">
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

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-title">
            Mecânica
        </div>
        """,
        unsafe_allow_html=True
    )
    sell_in = mecanica_mes[
        mecanica_mes["Tipo"]
        .astype(str)
        .str.upper()
        == "SELL IN"
    ]
    
    sell_out = mecanica_mes[
        mecanica_mes["Tipo"]
        .astype(str)
        .str.upper()
        == "SELL OUT"
    ]
    
    html = "<div class='mecanica-box'>"
    
    if not sell_in.empty:
    
        html += """
        <div class='mecanica-subtitle'>
            SELL IN
        </div>
        <ul class='mecanica-lista'>
        """
    
        for _, row in sell_in.iterrows():
            html += f"<li>{row['Texto']}</li>"
    
        html += "</ul>"
    
    if not sell_out.empty:
    
        html += """
        <div class='mecanica-subtitle'>
            SELL OUT
        </div>
        <ul class='mecanica-lista'>
        """
    
        for _, row in sell_out.iterrows():
            html += f"<li>{row['Texto']}</li>"
    
        html += "</ul>"
    
    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )

with col_direita:

    if produtos.empty:

        st.warning(
            "Nenhum produto encontrado."
        )

    else:

        mostrar_produtos(
            produtos,
            canal,
            negocio
        )


pdf_file = gerar_pdf(
    titulo=titulo,
    mes=mes,
    ano=ano,
    mecanica_mes=mecanica_mes,
    produtos=produtos,
    logo=logo
)

st.download_button(
    "📄 Exportar PDF",
    data=pdf_file,
    file_name=f"Calendario_{mes}_{ano}.pdf",
    mime="application/pdf"
)
