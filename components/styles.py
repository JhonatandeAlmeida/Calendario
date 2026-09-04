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
        min-height:200px;
        color:black;
    }

    .canal-title{
        background:#6E6E6E;
        color:white;
        text-align:center;
        font-size:26px;
        font-weight:bold;
        border-radius:5px;
        padding:10px;
        margin-top:20px;
        margin-bottom:15px;
    }

    .quinzena-title{
        background:#E8E8E8;
        color:black;
        text-align:center;
        font-size:18px;
        font-weight:bold;
        border-radius:5px;
        padding:8px;
        margin-top:10px;
        margin-bottom:15px;
    }

    .sku-name{
    text-align:center;
    font-size:14px;
    font-weight:bold;
    margin-top:8px;
    margin-bottom:8px;
    color:black;
    width:100%;
    }

    .old-price{
        background:#6E6E6E;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
    }

    .new-price{
        background:#B3B3B3;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
    }
    
    .mecanica-subtitle{
    background:#E8E8E8;
    color:black;
    text-align:center;
    font-weight:bold;
    padding:8px;
    border-radius:5px;
    margin-top:10px;
    margin-bottom:10px;
    }

    .mecanica-lista{
    margin-left:10px;
    margin-bottom:15px;
    }

    </style>
    """, unsafe_allow_html=True)
