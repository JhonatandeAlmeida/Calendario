def mostrar_produtos(df_canal, canal):

    st.markdown(
        f"""
        <div class='canal-title'>
            {canal}
        </div>
        """,
        unsafe_allow_html=True
    )

    for quinzena in sorted(df_canal["Quinzena"].unique()):

        st.markdown(
            f"""
            <div class='quinzena-title'>
                {quinzena}ª QUINZENA
            </div>
            """,
            unsafe_allow_html=True
        )

        produtos_q = df_canal[
            df_canal["Quinzena"] == quinzena
        ]

        cols = st.columns(6)

        for i, (_, row) in enumerate(produtos_q.iterrows()):

            with cols[i % 6]:

                try:
                    st.image(
                        f"images/produtos/{row['Imagem']}",
                        width=90
                    )
                except:
                    pass

                st.markdown(
                    f"""
                    <div class='sku-name'>
                        {row['SKU']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class='old-price'>
                        R$ {float(row['De']):.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class='new-price'>
                        R$ {float(row['Para']):.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


for canal in ["Atacado", "Varejo"]:

    df_canal = produtos[
        produtos["Canal"] == canal
    ]

    if len(df_canal) > 0:
        mostrar_produtos(df_canal, canal)
