with col2:

    st.markdown(
        """
        <div class="section-title">
            Mecânica
        </div>
        """,
        unsafe_allow_html=True
    )

    sell_in = mecanica_mes[
        mecanica_mes["Tipo"]
        .astype(str)
        .str.strip()
        .str.upper()
        == "SELL IN"
    ]

    sell_out = mecanica_mes[
        mecanica_mes["Tipo"]
        .astype(str)
        .str.strip()
        .str.upper()
        == "SELL OUT"
    ]

    html = "<div class='mecanica-box'>"

    if not sell_in.empty:

        html += """
        <div class='mecanica-subtitle'>
            SELL IN
        </div>
        <ul class='mecanica-lista'>
        """

        for _, row in sell_in.iterrows():
            html += f"<li>{row['Texto']}</li>"

        html += "</ul>"

    if not sell_out.empty:

        html += """
        <div class='mecanica-subtitle'>
            SELL OUT
        </div>
        <ul class='mecanica-lista'>
        """

        for _, row in sell_out.iterrows():
            html += f"<li>{row['Texto']}</li>"

        html += "</ul>"

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )
