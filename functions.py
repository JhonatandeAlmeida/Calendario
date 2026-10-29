import polars as pl
import pandas as pd
import re
import zipfile
import os
import glob
import streamlit as st
import datetime
import calendar
import pathlib
import time
import requests
from io import BytesIO


def read_excel_parquets(path: str, destino: str) -> None:
    """Lê o Excel e Salva em parquets"""
    sheets = get_excel_sheet_names(path)
    for sheet in sheets:
        if sheet in ["repasse", "cerveja", "depara_repasse"]:
            p = pd.read_excel(path, sheet_name=sheet)
            p.replace("-", "0.0")
            p.to_parquet(f"{destino}/{sheet}.parquet")

def get_excel_sheet_names(file_path):
    sheets = []
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        xml = zip_ref.read("xl/workbook.xml").decode("utf-8")
    for s_tag in re.findall("<sheet [^>]*", xml):
        sheets.append(re.search('name="[^"]*', s_tag).group(0)[6:])
    return sheets



HOSTNAME = "anheuserbuschinbev.sharepoint.com"
SITE_NAME = "ASCentroOeste"


@st.cache_resource
def get_access_token():

    url = (
        f"https://login.microsoftonline.com/"
        f"{st.secrets['TENANT_ID']}"
        "/oauth2/v2.0/token"
    )

    payload = {
        "grant_type": "client_credentials",
        "client_id": st.secrets["CLIENT_ID"],
        "client_secret": st.secrets["CLIENT_SECRET"],
        "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    response.raise_for_status()

    return response.json()["access_token"]


@st.cache_resource
def get_site_id():

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = (
        f"https://graph.microsoft.com/v1.0/sites/"
        f"{HOSTNAME}:/sites/{SITE_NAME}"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.json()["id"]


@st.cache_data(ttl=3600)
def baixar_arquivo_sharepoint(caminho_arquivo):

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    site_id = get_site_id()

    metadata_url = (
        f"https://graph.microsoft.com/v1.0/"
        f"sites/{site_id}"
        f"/drive/root:/{caminho_arquivo}"
    )

    response = requests.get(
        metadata_url,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()

    metadata = response.json()

    download_url = metadata[
        "@microsoft.graph.downloadUrl"
    ]

    arquivo = requests.get(
        download_url,
        timeout=120
    )

    arquivo.raise_for_status()

    return BytesIO(arquivo.content)
