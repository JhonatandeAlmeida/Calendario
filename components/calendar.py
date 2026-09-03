import calendar
import streamlit as st


def gerar_calendario(
    ano,
    mes,
    eventos=None
):

    if eventos is None:
        eventos = {}

    cal = calendar.monthcalendar(
        ano,
        mes
    )

    dias = [
        "DOM",
        "SEG",
        "TER",
        "QUA",
        "QUI",
        "SEX",
        "SAB"
    ]

    html = """
    <table style='width:100%; text-align:center; border-collapse:collapse'>
    """

    html += "<tr>"

    for dia in dias:

        html += f"""
        <th style="
            background:#EFEFEF;
            padding:8px;
            border:1px solid white;
        ">
            {dia}
        </th>
        """

    html += "</tr>"

    for semana in cal:

        html += "<tr>"

        for dia in semana:

            if dia == 0:

                html += """
                <td style='padding:12px'></td>
                """

            else:

                cor = "#DCE6F1"

                if dia in eventos:

                    if eventos[dia] == "Sell In":
                        cor = "#FCE4D6"

                    elif eventos[dia] == "Sell Out":
                        cor = "#FFF2CC"

                html += f"""
                <td style="
                    background:{cor};
                    padding:12px;
                    border:1px solid white;
                    font-weight:bold;
                ">
                    {dia}
                </td>
                """

        html += "</tr>"

    html += "</table>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )
