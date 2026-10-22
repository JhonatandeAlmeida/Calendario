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
