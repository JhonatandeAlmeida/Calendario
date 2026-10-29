import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64
import streamlit.components.v1 as components
from RepasseNAB import mostrar_repasse
from io import BytesIO
from components.styles import segmented_control_verde

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

import msal


CLIENT_ID = "2609a149-fd2a-409a-a4b6-700c940a1f74"
TENANT_ID = "cef04b19-7776-4a94-b89b-375c77a8f936"

QUERY_PARAMS = st.query_params

if "code" not in QUERY_PARAMS:

    login_url = (
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri=https://calendariogeoco.streamlit.app/"
        f"&scope=openid profile email User.Read"
    )

    st.title("Calendário Promocional")
    st.link_button("Entrar com Microsoft", login_url)
    st.stop()

st.success("Usuário autenticado")


@st.cache_data(ttl=30)
def imagem_para_base64(caminho):
    with open(caminho, "rb") as img:
        return base64.b64encode(
            img.read()
        ).decode("utf-8")

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
    ) * 0.95
    
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
    logo,
    canal,
    negocio,
    regional
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elementos = []

        # Logo

    try:
        caminho_logo = f"images/{logo}"
        img = Image.open(caminho_logo)
        largura_original, altura_original = img.size
        largura_desejada = 3* cm

        altura_proporcional = (
            largura_desejada * altura_original / largura_original
        )

        logo_pdf = PdfImage(
                caminho_logo,
                width=largura_desejada,
                height=altura_proporcional
                )
        

    except:
        pass

    elementos.append(logo_pdf)
    elementos.append(Spacer(1, 5))

    # Título

    cabecalho = Table(
        [[
            f"{titulo} | {canal} _ {regional} | {mes} {ano}"
        ]],
        colWidths=[18*cm]
    )
    
    cabecalho.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#005CB9")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 18),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 0, colors.white),
        ])
    )
    
    elementos.append(cabecalho)
    elementos.append(Spacer(1, 5))

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

    elementos.append(Spacer(1, 5))

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

    elementos.append(Spacer(1, 5))

    # Produtos

    df_canal = produtos.copy()
    
    quinzenas = sorted(
        df_canal["Quinzena"]
        .dropna()
        .astype(str)
        .unique()
    )
    
    for quinzena in sorted(quinzenas):

        titulo_quinzena = (
            f"{quinzena}ª QUINZENA"
            if (quinzena == "1" or quinzena == "2")
            else f"{quinzena}"
        )
        
        elementos.append(
            Paragraph(
                f"<b>{titulo_quinzena}</b>",
                styles["Heading3"]
            )
        )
      
        dados = [
            [
                "SKU",
                "DE",
                "POR"
            ]
        ]

        produtos_q = df_canal[
            df_canal["Quinzena"].astype(str) == str(quinzena)
        ]

        for _, row in produtos_q.iterrows():

            if (negocio == "MERCAPROMO" or isinstance(row["De"], str)):
                dados.append(
                    [
                        str(row["SKU"]),
                        f"R$ {row['De']}",
                        f"R$ {row['Para']}"
                    ]

                )
            else:
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
        estilo = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#005CB9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]
        
        for i in range(1, len(dados)):
            if i % 2 == 0:
                estilo.append(
                    ("BACKGROUND", (0, i), (-1, i), colors.whitesmoke)
                )
        
        tabela.setStyle(
            TableStyle(estilo)
        )

        elementos.append(tabela)
        elementos.append(Spacer(1, 5))

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

espp1, colp1, espp2 = st.columns([2,8,1])

with colp1:

    segmented_control_verde()

    st.markdown(
        '<div class="modulo-menu">',
        unsafe_allow_html=True
    )
    
    pagina = st.segmented_control(
        "",
        options=[
            "Calendário",
            "Mercapromo",
            "Árvore de Preços",
            "Repasse NAB"
        ],
        default="Calendário"
    )
    
    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
    

# ==================================================
# PRODUTOS
# ==================================================

def mostrar_produtos(df_canal, canal, negocio, regional):

    st.markdown(
        f"""
        <div class="canal-title">
            {canal} - {regional}
        </div>
        """,
        unsafe_allow_html=True
    )

    quinzenas = sorted(
        df_canal["Quinzena"]
        .dropna()
        .astype(str)
        .unique()
    )
    max_skus = (
        df_canal.groupby("Quinzena")
        .size()
        .max()
    )

    for quinzena in quinzenas:

        if (quinzena == "1" or quinzena == "2"):
            st.markdown(
            f"""
            <div class="quinzena-title">
                {quinzena}ª QUINZENA
            </div>
            """,
            unsafe_allow_html=True
        )
        else:
            st.markdown(
            f"""
            <div class="quinzena-title">
                {quinzena}
            </div>
            """,
            unsafe_allow_html=True
        )

        if negocio == "MERCAPROMO" :
            produtos_q = (
                    df_canal[
                        df_canal["Quinzena"].astype(str) == str(quinzena)
                    ]
                )
        else:
            df_temp = df_canal[
                df_canal["Quinzena"].astype(str) == str(quinzena)
            ].copy()
            
            df_temp["Para_Ordenacao"] = pd.to_numeric(
                df_temp["Para"],
                errors="coerce"
            )
            
            produtos_q = df_temp.sort_values(
                by="Para_Ordenacao",
                ascending=True,
                na_position="last"
            )
            

        qtd_skus = len(produtos_q)

        # Centraliza os produtos em relação à quinzena com mais SKUs
        offset = max((max_skus - qtd_skus) // 2, 0)
        
        cols = st.columns(max_skus)


        for i, (_, row) in enumerate(produtos_q.iterrows()):

            with cols[i + offset]:
                if (negocio == "MERCAPROMO" or isinstance(row["De"], str)):
                    preco_de = row["De"]
                    preco_para = row["Para"]
                    
                else:
                    preco_de = float(row["De"])
                    preco_para = float(row["Para"])
    
                    delta_rs = preco_de - preco_para

                try:

                    caminho_img = (
                        f"images/produtos_padronizados/{row['Imagem']}"
                    )
                
                    img_base64 = imagem_para_base64(caminho_img)
                
                    largura_imagem = 220
                
                    st.markdown(
                        f"""
                        <div style="
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            width: 100%;
                            margin-bottom: 10px;
                        ">
                            <img src="data:image/png;base64,{img_base64}" style="width: 110px; max-width: 100%;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                except Exception as e:
                    st.write(e)



                st.markdown(
                    f"""
                    <div class="sku-name">
                        {row['SKU']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if (negocio == "MERCAPROMO" or isinstance(row["De"], str)):
                    st.markdown(
                        f"""
                        <div class="delta-nok">
                           -
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
                     st.markdown(
                        f"""
                        <div class="delta-price">
                            ↓ R$ {delta_rs:.2f}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                if (negocio == "MERCAPROMO" or isinstance(row["De"], str)):
                    st.markdown(
                        f"""
                        <div class="old-price">
                            {preco_de}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
                    st.markdown(
                        f"""
                        <div class="new-price">
                            {preco_para}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
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
                                
if pagina == "Calendário":

    # ==================================================
    # LEITURA DA PLANILHA
    # ==================================================

    ARQUIVO = "data/calendario_promocional.xlsx"

    @st.cache_data(ttl=30)
    def carregar_planilha():

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

        return (
            config_df,
            cal_df,
            mec_df,
            prod_df
        )

    try:

        config_df, cal_df, mec_df, prod_df = carregar_planilha()

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
        if os.path.exists(destino):
            continue
            
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

    meses = sorted(
        prod_df["Mes"]
        .dropna()
        .astype(str)
        .unique(),
        key=lambda x: meses_mapa.get(x, 99)
    )


    colf1, colf2, esp1, colf3, colf4,  esp2, colf5, colf6, esp3, colf7, colf8 = st.columns([0.4,2,0.4,0.4,2,0.4,0.4,2,0.4,0.4,2])

    with colf1:
        st.markdown(
            "<div style='font-size:18px;font-weight:bold;margin-bottom:1px'>          Mês</div>",
            unsafe_allow_html=True
        )
    with colf2:
        mes = st.selectbox(
            "Mês",
            meses,
            label_visibility="collapsed",
            index=meses.index(mes_padrao)
            if mes_padrao in meses else 0
        )

    with colf3:
        st.markdown(
            "<div style='font-size:18px;font-weight:bold;margin-bottom:1px'>          Tipo</div>",
            unsafe_allow_html=True
        )
    with colf4:
        negocios = sorted(
            prod_df["Tipo"]
            .dropna()
            .astype(str)
            .unique()
        )
        negocio = st.selectbox(
            "Tipo",
            negocios,
            label_visibility="collapsed",
        )
        
    with colf5:
        st.markdown(
            "<div style='font-size:18px;font-weight:bold;margin-bottom:1px'>          UF</div>",
            unsafe_allow_html=True
        )
    with colf6:
        regionais = sorted(
            prod_df.loc[
                prod_df["Tipo"] == negocio,
                "Regional"
            ]
            .dropna()
            .astype(str)
            .unique()
        )
        regional = st.selectbox(
            "Regional",
            regionais,
            label_visibility="collapsed",
            index=regionais.index(regional_padrao)
            if regional_padrao in regionais else 0
        )
        
    with colf7:
        st.markdown(
            "<div style='font-size:18px;font-weight:bold;margin-bottom:1px'>     Canal</div>",
            unsafe_allow_html=True
        )
    with colf8:
        
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
            label_visibility="collapsed",
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

    mes_numero = meses_mapa.get(
        mes,
        9
    )

    cal_mes = cal_df[
        (cal_df["Data"].dt.month == mes_numero)
        &
        (cal_df["Data"].dt.year == ano)
        &
        (cal_df["SKU"].astype(str) == negocio)
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

        merca = mecanica_mes[
            mecanica_mes["Tipo"]
            .astype(str)
            .str.upper()
            == "MERCAPROMO"
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

        if not merca.empty:
        
            html += """
            <div class='mecanica-subtitle'>
                MERCAPROMO
            </div>
            <ul class='mecanica-lista'>
            """
        
            for _, row in merca.iterrows():
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
                negocio,
                regional
            )

    pdf_file = gerar_pdf(
        titulo=titulo,
        mes=mes,
        ano=ano,
        mecanica_mes=mecanica_mes,
        produtos=produtos,
        logo=logo,
        canal=canal,
        negocio=negocio,
        regional=regional
    )

    st.download_button(
        "📄 Exportar PDF",
        data=pdf_file,
        file_name=f"Calendario_{canal}_{regional}_{mes}_{ano}.pdf",
        mime="application/pdf"
    )

elif pagina == "Calendário Mercapromo":


    st.title("Calendário Mercapromo")


    with open(
        "calendario_mercapromo.html",
        "r",
        encoding="utf-8"
    ) as f:
        html = f.read()


    components.html(
        html,
        height=2500,
        scrolling=True
    )
elif pagina ==  "Árvore de Preços + Repasse Cerv":

    #st.title("Árvore de Preços + Repasse")
    col_title, col_logo = st.columns([8, 1])

    with col_title:

        st.markdown(
            f"""
            <div class="main-title">
                Resumo Repasse - {pagina}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_logo:

        try:
            st.image(
                f"images/logo.png",
                width=120
            )
        except:
            pass

    with open(
        "arvore_de_preços_e_repasse.html",
        "r",
        encoding="utf-8"
    ) as f:
        html = f.read()

    components.html(
        html,
        height=2500,
        scrolling=True
    )
else:
    mostrar_repasse()
