import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .main-title{
        font-size:42px;
        font-weight:bold;
        color:#0066B3;
        margin-bottom:20px;
    }

    .month-title{
        color:black;
        font-size:36px;
    }

    .section-title{
        background:#737373;
        color:white;
        text-align:center;
        border-radius:5px;
        padding:8px;
        font-size:28px;
        font-weight:bold;
        margin-bottom:10px;
    }

    .card-container{
        background:#EEF1F5;
        border-radius:20px;
        padding:20px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.15);
        margin-bottom:15px;
    }

    .sku-name{
        text-align:center;
        font-weight:bold;
        font-size:14px;
        margin-top:5px;
    }

    .old-price{
        background:#7F7F7F;
        color:white;
        border-radius:18px;
        text-align:center;
        padding:4px;
        margin-top:5px;
    }

    .new-price{
        background:#BBBBBB;
        color:white;
        border-radius:18px;
        text-align:center;
        padding:4px;
        margin-top:5px;
    }

    .canal-title{
        text-align:center;
        font-weight:bold;
        font-size:24px;
        background:white;
        border-radius:8px;
        padding:5px 15px;
        width:180px;
        margin:auto;
        box-shadow:0px 2px 5px rgba(0,0,0,0.2);
    }

    .mecanica-box{
        border:1px solid #D0D0D0;
        padding:20px;
        border-radius:5px;
        background:white;
    }

    </style>
    """, unsafe_allow_html=True)
