#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:33:35 2025

@author: fran
"""
import os
import pandas as pd
import numpy as np


#FOLDER = r"/home/fran/Desktop/Stamm/"   # <-- pon tu carpeta aquí (puede ser relativa o absoluta)
def read_all_csvs(folder: str) -> pd.DataFrame:
    CSV_EXT = ".csv"
    CSV_READ_KW = dict(
        sep=";",          # cambia a "," si tus CSV usan coma
        dtype={
        "TIME": "string",
        "ISIN": "category",
        "PRODUCT TYPE": "category",
        "ISSUER": "category",
        "UNDERLYING": "category",
        },
        converters={
        "PRICE": lambda x: float(str(x).replace(",", ".")) if x else np.nan,
        "VOLUME": lambda x: float(str(x).replace(",", ".")) if x else np.nan,
        },
        quotechar='"',
        on_bad_lines="skip",
        engine="python"
    )
    
    
    csv_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(CSV_EXT):
                csv_files.append(os.path.join(root, f))

    if not csv_files:
        raise FileNotFoundError(f"No se encontraron {CSV_EXT} en: {folder}")

    frames, errors = [], []
    for path in csv_files:
        try:
            frames.append(pd.read_csv(path, **CSV_READ_KW))
        except Exception as e:
            errors.append(f"{os.path.basename(path)} → {e}")

    if not frames:
        raise RuntimeError("No se pudo leer ningún CSV.\n" + "\n".join(errors[:5]))

    df = pd.concat(frames, ignore_index=True, sort=False)
    return df, errors
