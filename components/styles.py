import streamlit as st


def load_css():

    st.markdown("""
    <style>

    .main-title{
        font-size:42px;
        font-weight:700;
        color:#0066B3;
        margin-bottom:20px;
    }

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

    .mecanica-box{
    background:white;
    border:1px solid #CFCFCF;
    border-radius:5px;
    padding:15px;
    min-height:200px;
    color:black;
    font-size:16px;
    }

    .canal-title{
        width:200px;
        margin:auto;
        text-align:center;
        background:white;
        padding:8px;
        font-size:26px;
        font-weight:bold;
        border-radius:10px;
        box-shadow:0px 2px 8px rgba(0,0,0,.20);
    }

    .sku-name{
        text-align:center;
        font-size:14px;
        font-weight:bold;
        margin-top:5px;
        min-height:40px;
    }

    .old-price{
        background:#7C7C7C;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
    }

    .new-price{
        background:#B9B9B9;
        color:white;
        text-align:center;
        padding:5px;
        border-radius:20px;
        margin-top:5px;
    }

    </style>
    """,
    unsafe_allow_html=True)
