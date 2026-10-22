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
