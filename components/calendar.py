import calendar
import pandas as pd
import streamlit as st


def gerar_calendario(ano, mes, eventos=None):

    if eventos is None:
        eventos = {}

    calendar.setfirstweekday(calendar.SUNDAY)

    semanas = calendar.monthcalendar(ano, mes)

    linhas = []

    for semana in semanas:

        linha = []

        for dia in semana:

            if dia == 0:
                linha.append("")
            else:

                if dia in eventos:

                    if eventos[dia] == "1ª QUINZ":
                        linha.append(f"🟧 {dia}")

                    elif eventos[dia] == "2ª QUINZ":
                        linha.append(f"🟨 {dia}")

                    else:
                        linha.append(str(dia))

                else:
                    linha.append(str(dia))

        linhas.append(linha)

    df = pd.DataFrame(
        linhas,
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
    🟧 Sell In &nbsp;&nbsp;&nbsp;&nbsp;
    🟨 Sell Out
    """)
