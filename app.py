import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    layout="wide",
    page_title="Calendário Promocional"
)

# Dados
produtos = pd.read_excel("data/produtos.xlsx")
mecanica = pd.read_excel("data/mecanica.xlsx")

st.title("📅 Calendário | Setembro 2026")

col1, col2 = st.columns([1,1.2])

# CALENDÁRIO
with col1:
    st.subheader("Setembro")

    calendario_html = """
    <table style='width:100%; text-align:center'>
    <tr>
    <th>DOM</th>
    <th>SEG</th>
    <th>TER</th>
    <th>QUA</th>
    <th>QUI</th>
    <th>SEX</th>
    <th>SAB</th>
    </tr>
    </table>
    """

    st.markdown(calendario_html, unsafe_allow_html=True)

# MECÂNICA
with col2:
    st.subheader("Mecânica")

    for texto in mecanica["Mecânica"]:
        st.markdown(f"• {texto}")
