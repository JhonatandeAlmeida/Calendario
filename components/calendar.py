import calendar
import pandas as pd
import streamlit as st


def gerar_calendario(ano, mes, eventos=None):

    if eventos is None:
        eventos = {}

    calendar.setfirstweekday(calendar.SUNDAY)

    semanas = calendar.monthcalendar(ano, mes)

    dados = []

    for semana in semanas:

        linha = []

        for dia in semana:

            if dia == 0:
                linha.append("")

            elif dia in eventos:

                if eventos[dia] == "Sell In":
                    linha.append(f"🟧 {dia}")

                elif eventos[dia] == "Sell Out":
                    linha.append(f"🟨 {dia}")

                else:
                    linha.append(str(dia))

            else:
                linha.append(str(dia))

        dados.append(linha)

    df = pd.DataFrame(
        dados,
        columns=[
            "DOM",
            "SEG",
            "TER",
            "QUA",
            "QUI",
            "SEX",
            "SAB"
        ]
    )

    st.table(df)

    st.markdown("""
    🟧 1ª QUINZENA &nbsp;&nbsp;&nbsp;&nbsp;
    🟨 2ª QUINZENA
    """)
