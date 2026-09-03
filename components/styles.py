import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* TÍTULO PRINCIPAL */
    .main-title{
        font-size:42px;
        font-weight:700;
        color:#0066B3;
        margin-bottom:20px;
    }

    /* CABEÇALHOS DE SEÇÃO */
    .section-title{
        background:#6E6E6E;
        color:white;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        border-radius:4px;
        padding:8px;
        margin-bottom:5px;
    }

    /* CAIXA DE MECÂNICA */
    .mecanica-box{
        background:white;
        border:1px solid #CFCFCF;
        border-radius:5px;
        padding:15px;
        min-height:220px;
        color:black;
        font-size:16px;
    }

    .mecanica-box ul{
        margin:0;
        padding-left:20px;
    }

    .mecanica-box li{
        margin-bottom:10px;
        line-height:1.5;
    }

    /* TÍTULO DOS CANAIS */
    .canal-title{
        width:220px;
        margin:auto;
        text-align:center;
        background:white;
        color:black;
        padding:8px;
        font-size:26px;
        font-weight:bold;
        border-radius:10px;
        box-shadow:0px 2px 8px rgba(0,0,0,.20);
    }

    /* NOME SKU */
    .sku-name{
        text-align:center;
        font-size:14px;
        font-weight:bold;
        margin-top:5px;
        min-height:40px;
        color:black;
    }

    /* PREÇO DE */
    .old-price{
        background:#7C7C7C;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
        font-weight:bold;
    }

    /* PREÇO PARA */
    .new-price{
        background:#B9B9B9;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
        font-weight:bold;
    }

    /* IMAGENS DOS PRODUTOS */
    [data-testid="stImage"]{
        text-align:center;
    }

    </style>
    """,
    unsafe_allow_html=True)
