import calendar
import streamlit as st


def gerar_calendario(ano, mes, eventos=None):

    if eventos is None:
        eventos = {}

    # Semana começa no domingo
    calendar.setfirstweekday(calendar.SUNDAY)

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
    <table style="
        width:100%;
        border-collapse:collapse;
        text-align:center;
        font-family:Arial;
    ">
    """

    # Cabeçalho
    html += "<tr>"

    for dia in dias_semana:

        html += f"""
        <th style="
            background:#E6E6E6;
            padding:8px;
            border:1px solid white;
            font-size:14px;
        ">
            {dia}
        </th>
        """

    html += "</tr>"

    # Dias do mês
    for semana in cal:

        html += "<tr>"

        for dia in semana:

            if dia == 0:

                html += """
                <td style="
                    height:40px;
                    border:1px solid white;
                ">
                </td>
                """

            else:

                # Cor padrão
                cor = "#DCE6F1"

                if dia in eventos:

                    if eventos[dia] == "Sell In":
                        cor = "#FCE4D6"

                    elif eventos[dia] == "Sell Out":
                        cor = "#FFF2CC"

                html += f"""
                <td style="
                    background:{cor};
                    height:40px;
                    border:1px solid white;
                    font-weight:bold;
                    font-size:15px;
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
