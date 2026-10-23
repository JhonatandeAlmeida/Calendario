import base64
import io
import os
from pathlib import Path

import altair as alt
import pandas as pd
import polars as pl
import streamlit as st
from PIL import Image
from pandas.api.types import is_numeric_dtype
from components.styles import load_css

from functions import read_excel_parquets

def mostrar_repasse():
    # ============================================================
    # CONFIGURAÇÕES
    # ============================================================
    
    TITLE = "NOVEMBRO/26 - VIG: 09/11"
    
    CANAL_CONFIG = {
        "BAR": {
            "y": "rota-ttc pos",
            "pre": "rota-ttv pre",
            "pos": "rota-ttv pos",
            "delta": "rota-delta ttv",
            "pre_label": "TTV Pré",
            "pos_label": "TTV Pós",
            "delta_label": "Delta TTV",
            "extra": "rota-ttc pos",
            "extra_label": "TTC Pós",
        },
        "ASR": {
            "y": "asr-ttc pos",
            "pre": "asr-ttv pre",
            "pos": "asr-ttv pos",
            "delta": "asr-delta ttv",
            "pre_label": "TTV Pré",
            "pos_label": "TTV Pós",
            "delta_label": "Delta TTV",
            "extra": "asr-ttc pos",
            "extra_label": "TTC Pós",
        },
        "VAREJO": {
            "y": "varejo-ttc pos",
            "pre": "varejo-ttc pre",
            "pos": "varejo-ttc pos",
            "delta": "varejo-delta ttc",
            "pre_label": "Pré",
            "pos_label": "Pós",
            "delta_label": "TTC",
        },
        "ATACADO": {
            "y": "atacado-ttc pos",
            "pre": "atacado-ttc pre",
            "pos": "atacado-ttc pos",
            "delta": "atacado-delta ttc",
            "pre_label": "Pré",
            "pos_label": "Pós",
            "delta_label": "Delta",
        },
    }
    
    CANAIS = {
        "BAR": [
            "rota-ttv pre",
            "rota-ttv pos",
            "rota-delta ttv",
            "rota-ttc pos",
        ],
        "ASR": [
            "asr-ttv pre",
            "asr-ttv pos",
            "asr-delta ttv",
            "asr-ttc pos",
        ],
        "VAREJO": [
            "varejo-ttc pre",
            "varejo-ttc pos",
            "varejo-delta ttc",
        ],
        "ATACADO": [
            "atacado-ttc pre",
            "atacado-ttc pos",
            "atacado-delta ttc",
        ],
    }
    
    COMUM = [
        "uf",
        "geo",
        "emb.",
        "sku",
        "qtd cx",
        "nome_slide",
        "grupo",
        "nome",
        "marca",
        "caminho",
    ]
    
    
    # ============================================================
    # UTILITÁRIOS
    # ============================================================
    
    @st.cache_data(ttl=30)
    def convert_image(path):
    
        if not path:
            return None
    
        path = str(path).replace("\\", "/")
    
        if not os.path.exists(path):
            return None
    
        try:
            with Image.open(path) as image:
    
                output = io.BytesIO()
    
                image.save(
                    output,
                    format="PNG"
                )
    
            return (
                "data:image/png;base64,"
                + base64.b64encode(
                    output.getvalue()
                ).decode()
            )
    
        except Exception:
            return None
    
    
    def moeda(series):
    
        return (
            "R$ "
            + series.round(2)
            .map("{:,.2f}".format)
            .astype(str)
        )
    
    
    # ============================================================
    # CARREGAMENTO DOS DADOS
    # ============================================================
    
    @st.cache_data(ttl=30, show_spinner=False)
    def load_data():
    
        read_excel_parquets(
            "data/repasse/graficos.xlsx",
            "data/repasse",
        )
    
        repasse = pl.read_parquet(
            "data/repasse/repasse.parquet"
        )
    
        depara = pl.read_parquet(
            "data/repasse/depara_repasse.parquet"
        )
    
        if "Caminho" in depara.columns:
    
            depara_pd = depara.to_pandas()
    
            depara_pd["Caminho"] = (
                depara_pd["Caminho"]
                .fillna("")
                .apply(convert_image)
            )
    
            depara = pl.from_pandas(depara_pd)
    
        repasse = repasse.join(
            depara,
            on="SKU",
            how="left",
        )
    
        repasse.columns = [
            c.lower()
            for c in repasse.columns
        ]
    
        return repasse
    
    
    # ============================================================
    # PREPARAÇÃO DOS DADOS
    # ============================================================
    
    def prepare_dataframe(
        df: pd.DataFrame,
        canal: str,
    ):
    
        cfg = CANAL_CONFIG[canal]
    
        df = df.copy()
    
        df["line1"] = df["nome_slide"]
    
        df["line2"] = (
            cfg["pre_label"]
            + ": "
            + moeda(df[cfg["pre"]])
        )
    
        df["line3"] = (
            cfg["pos_label"]
            + ": "
            + moeda(df[cfg["pos"]])
        )
    
        df["line_delta"] = (
            cfg["delta_label"]
            + ": "
            + moeda(df[cfg["delta"]])
        )
    
        if "extra" in cfg:
    
            df["line4"] = (
                cfg["extra_label"]
                + ": "
                + moeda(df[cfg["extra"]])
            )
    
        return df
    
    
    # ============================================================
    # COMPONENTES ALTAIR
    # ============================================================
    
    def make_text(
        df,
        texto,
        fonte,
        offset,
        x,
        y,
        canal,
        color="black",
        weight="normal",
    ):
    
        delta_col = CANAL_CONFIG[canal]["delta"]
    
        chart = alt.Chart(df).mark_text(
            align="center",
            dy=offset,
            size=fonte,
            color=color,
            fontWeight=weight,
        )
    
        if texto == "line_delta":
    
            return chart.encode(
                x=f"{x}:N",
                y=alt.Y(y, axis=None),
                text=texto,
                color=alt.condition(
                    alt.datum[delta_col] <= 0,
                    alt.value("green"),
                    alt.value("red"),
                ),
            )
    
        return chart.encode(
            x=f"{x}:N",
            y=alt.Y(y, axis=None),
            text=texto,
        )
    
    
    def make_graph_repasse(
        df,
        canal,
        chart_height=250,
        chart_width=1600,
        image_height=120,
    ):
    
        if df.empty:
            return alt.Chart(pd.DataFrame())
    
        cfg = CANAL_CONFIG[canal]
    
        df = prepare_dataframe(
            df,
            canal,
        )
    
        y_col = cfg["y"]
    
        df["nome_sorted"] = (
            df[y_col]
            .fillna(0)
            .map(lambda x: f"{x:010.2f}")
            + "_"
            + df["nome_slide"]
        )
    
        y_min = df[y_col].min()
        y_max = df[y_col].max()
    
        image_chart = (
            alt.Chart(df)
            .mark_image(
                height=image_height,
                baseline="bottom",
            )
            .encode(
                x=alt.X(
                    "nome_sorted:N",
                    axis=None,
                ),
                y=alt.Y(
                    f"{y_col}:Q",
                    axis=alt.Axis(
                        labels=False,
                        title="",
                        grid=False,
                    ),
                    scale=alt.Scale(
                        domain=[
                            y_min - 0.5,
                            y_max + 0.5,
                        ]
                    ),
                ),
                url="caminho",
            )
            .properties(
                height=chart_height,
                width=chart_width,
            )
        )
    
        tick = image_chart.mark_tick(
            color="black",
            thickness=2,
            yOffset=20,
            size=max(
                30,
                chart_width / max(len(df), 1) - 50,
            ),
        )
    
        layers = [image_chart, tick]
    
        line_columns = sorted(
            [
                c
                for c in df.columns
                if c.startswith("line")
            ]
        )
    
        for idx, column in enumerate(line_columns):
    
            layers.append(
                make_text(
                    df=df,
                    texto=column,
                    fonte=15,
                    offset=35 + (idx * 18),
                    x="nome_sorted",
                    y=y_col,
                    canal=canal,
                    weight="bold" if idx == 0 else "normal",
                )
            )
    
        return alt.layer(*layers)
    
    
    # ============================================================
    # APP
    # ============================================================
    load_css()
    
    st.set_page_config(
        page_title=f"PINC NAB - {TITLE}",
        page_icon="📈",
        layout="wide"
    )

        
    st.markdown(
        """
        <style>
            div.block-container {
                padding-top: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    #st.header(f"Resumo Repasse - {TITLE}")
    # ==================================================
    # CABEÇALHO
    # ==================================================

    col_title, col_logo = st.columns([8, 1])

    with col_title:

        st.markdown(
            f"""
            <div class="main-title">
                Resumo Repasse - {TITLE}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_logo:

        try:
            st.image(
                f"images/logo.png",
                width=120
            )
        except:
            pass
    
    repasse = load_data()
    
    resumo_canais = (
        repasse.select(
            [
                "uf",
                "geo",
                "sku",
                "varejo-ttc pos",
                "atacado-ttc pos",
            ]
        )
    )
    
    resumo_canais.columns = [
        "UF",
        "Geo",
        "SKU",
        "VAREJO",
        "ATACADO",
    ]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
    
        uf = st.segmented_control(
            "UF",
            sorted(repasse["uf"].unique()),
            default="DF",
        )
    
    with col2:
    
        canal = st.segmented_control(
            "Canal",
            [
                "VAREJO",
                "ATACADO",
            ],
            default="VAREJO",
        )
    
    repasse_filtrado = (
        repasse
        .filter(pl.col("uf") == uf)
        .select(
            COMUM + CANAIS[canal]
        )
        .to_pandas()
    )
    
    graphs = []
    
    for grupo in [
        "Single",
        "Premium",
        "Multi1",
        "Multi2",
    ]:
    
        df_grupo = repasse_filtrado[
            repasse_filtrado["grupo"] == grupo
        ]
    
        if len(df_grupo):
    
            graphs.append(
                make_graph_repasse(
                    df_grupo,
                    canal,
                )
            )
    
    if graphs:
    
        graph = alt.vconcat(*graphs).properties(
            title=alt.Title(
                f"{canal.title()} - {uf}",
                fontSize=30,
                fontWeight="bold",
            )
        )
    
        st.altair_chart(
            graph,
            use_container_width=True,
        )
    
    tab1, tab2 = st.columns(2)
    
    with tab1:
    
        st.dataframe(
            repasse_filtrado.drop(
                columns=[
                    "emb.",
                    "qtd cx",
                    "nome_slide",
                    "grupo",
                    "nome",
                    "marca",
                    "caminho",
                ],
                errors="ignore",
            ),
            hide_index=True,
            use_container_width=True,
            height=2000,
            column_config={
                col: st.column_config.NumberColumn(
                    label=col.split("-")[-1].upper(),
                    format="R$ %.2f",
                )
                for col in repasse_filtrado.columns
                if is_numeric_dtype(
                    repasse_filtrado[col]
                )
            },
        )
    
    with tab2:
    
        st.dataframe(
            resumo_canais
            .filter(pl.col("UF") == uf)
            .to_pandas(),
            hide_index=True,
            use_container_width=True,
            height=2000,
            column_config={
                "UF": "Estado",
                "VAREJO": st.column_config.NumberColumn(
                    "Varejo",
                    format="R$ %.2f",
                ),
                "ATACADO": st.column_config.NumberColumn(
                    "Atacado",
                    format="R$ %.2f",
                ),
            },
        )
