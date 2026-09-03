st.markdown("## Atacado")

cols = st.columns(4)

atacado = produtos[
    produtos["Canal"]=="Atacado"
]

for i, row in enumerate(atacado.iterrows()):

    _, produto = row

    with cols[i % 4]:

        st.image(
            f"images/produtos/{produto['Imagem']}",
            width=90
        )

        st.markdown(
            f"""
            **{produto['SKU']}**

            🔵 R$ {produto['Preço Atual']}

            🟢 R$ {produto['Preço Promo']}
            """
        )
