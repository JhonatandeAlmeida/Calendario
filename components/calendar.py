import calendar
from datetime import datetime
import pandas as pd
import streamlit as st


def gerar_calendario(ano, mes, eventos=None):

    if eventos is None:
        eventos = {}

    cal = calendar.monthcalendar(ano, mes)

    dias_semana = [
        "DOM",
        "SEG",
        "TER",
        "QUA",
        "QUI",
        "SEX",
        "SAB"
    ]

    html = """
    <table style='width:100%;border-collapse:collapse;text-align:center'>
    """

    html += "<tr>"

    for dia in dias_semana:
        html += f"""
        <th style='padding:5px;background:#EFEFEF'>
        {dia}
        </th>
        """

    html += "</tr>"

    for semana in cal:

        html += "<tr>"

        for dia in semana:

            if dia == 0:
                html += "<td></td>"

            else:

                cor = "#DCE6F1"

                if dia in eventos:

                    if eventos[dia] == "Sell In":
                        cor = "#FCE4D6"

                    if eventos[dia] == "Sell Out":
                        cor = "#FFF2CC"

                html += f"""
                <td
                style='
                    background:{cor};
                    padding:10px;
                    border:1px solid white;
                    font-weight:bold;
                '>
                    {dia}
                </td>
                """

        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)
