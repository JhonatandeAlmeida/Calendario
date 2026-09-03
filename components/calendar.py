import calendar
import streamlit as st


def gerar_calendario(ano, mes, eventos=None):

    if eventos is None:
        eventos = {}

    calendar.setfirstweekday(calendar.SUNDAY)

    semanas = calendar.monthcalendar(ano, mes)

    html = """
    <table style="
        width:100%;
        border-collapse:collapse;
        text-align:center;
        font-family:Arial;
        font-size:14px;
    ">
    """

    # Cabeçalho
    html += """
    <tr>
        <th style="padding:10px;border:1px solid #D9D9D9;">DOM</th>
        <th style="padding:10px;border:1px solid #D9D9D9;">SEG</th>
        <th style="padding:10px;border:1px solid #D9D9D9;">TER</th>
        <th style="padding:10px;border:1px solid #D9D9D9;">QUA</th>
        <th style="padding:10px;border:1px solid #D9D9D9;">QUI</th>
        <th style="padding:10px;border:1px solid #D9D9D9;">SEX</th>
        <th style="padding:10px;border:1px solid #D9D9D9;">SAB</th>
    </tr>
    """

    # Dias
    for semana in semanas:

        html += "<tr>"

        for dia in semana:

            if dia == 0:

                html += """
                <td style="
                    height:55px;
                    border:1px solid #D9D9D9;
                    background:white;
                ">
                </td>
                """

            else:

                cor = "#FFFFFF"

                if dia in eventos:

                    if eventos[dia] == "1ª QUINZ":
                        cor = "#F4B183"  # laranja

                    elif eventos[dia] == "2ª QUINZ":
                        cor = "#FFD966"  # amarelo

  
