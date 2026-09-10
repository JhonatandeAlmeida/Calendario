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
        border-radius:8px;
        padding:15px;
        min-height:250px;
        color:black;
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
        padding-left:20px;
        margin-bottom:15px;
    }

    .mecanica-lista li{
        margin-bottom:8px;
        color:black;
    }

    .canal-title{
        background:#6E6E6E;
        color:white;
        text-align:center;
        font-size:22px;
        font-weight:bold;
        border-radius:5px;
        padding:8px;
        margin-bottom:10px;
    }

    .quinzena-title{
        background:#E8E8E8;
        color:black;
        text-align:center;
        font-size:18px;
        font-weight:bold;
        border-radius:5px;
        padding:6px;
        margin-top:5px;
        margin-bottom:15px;
    }

    .produto-card{
        text-align:center;
        padding:10px;
        margin-bottom:2px;
    }

    .sku-name{
        text-align:center;
        font-size:18px;
        font-weight:bold;
        color:black;
        margin-top:2px;
        margin-bottom:2px;
        min-height:25px;
    }
    
    .old-price{
        background:#6E6E6E;
        color:white;
        text-align:center;
        border-radius:20px;
        padding:6px;
        width:80%;
        margin:5px auto;
    }
    
    .new-price{
        background:#B3B3B3;
        color:white;
        text-align:center;
        border-radius:20px;
        padding:6px;
        width:80%;        
        margin-bottom:10px;
        margin:5px auto;
    }
    [data-testid="stImage"]{
        text-align:center;
    }

    .delta-price{
    background:#E8F5E9;
    color:#00A651;
    border-radius:12px;
    width:70%;
    margin:4px auto 8px auto;
    padding:4px;
    text-align:center;
    font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)
