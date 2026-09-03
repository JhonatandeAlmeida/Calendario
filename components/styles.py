import streamlit as st


def load_css():

    st.markdown("""
    <style>

    .main-title{
        font-size:40px;
        font-weight:700;
        color:#0066B3;
        margin-bottom:20px;
    }

    .section-title{
        background:#6E6E6E;
        color:white;
        text-align:center;
        font-size:22px;
        font-weight:bold;
        border-radius:5px;
        padding:8px;
        margin-bottom:10px;
    }

    .mecanica-box{
        background:white;
        border:1px solid #CFCFCF;
        border-radius:5px;
        padding:15px;
        min-height:220px;
        color:black;
    }

    .canal-title{
        width:220px;
        margin:auto;
        text-align:center;
        background:white;
        color:black;
        padding:8px;
        font-size:24px;
        font-weight:bold;
        border-radius:10px;
        box-shadow:0px 2px 5px rgba(0,0,0,0.2);
    }

    .sku-name{
        text-align:center;
        color:black;
        font-weight:bold;
        min-height:40px;
    }

    .old-price{
        background:#686868;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
    }

    .new-price{
        background:#B5B5B5;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
    }

    </style>
    """, unsafe_allow_html=True)
