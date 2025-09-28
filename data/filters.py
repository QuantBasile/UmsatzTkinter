#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:46:26 2025

@author: fran
"""

import pandas as pd

def filter_by_issuers(df: pd.DataFrame, issuers: list[str] | None) -> pd.DataFrame:
    if not issuers:  # None or empty -> no filter
        return df
    return df[df["ISSUER"].isin(issuers)]


def _ensure_time_dt(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asegura una columna caché TIME_DT (datetime64[ns]) para filtrar rápido.
    No modifica TIME (string), solo añade/corrige TIME_DT si falta.
    """
    if "TIME_DT" not in df.columns or not pd.api.types.is_datetime64_any_dtype(df["TIME_DT"]):
        df = df.copy()
        df["TIME_DT"] = pd.to_datetime(df["TIME"], errors="coerce", dayfirst=True, cache=True)
    return df

def filter_by_time(df: pd.DataFrame, start: str | pd.Timestamp | None, end: str | pd.Timestamp | None) -> pd.DataFrame:
    if start is None and end is None:
        return df
    df = _ensure_time_dt(df)
    s = pd.to_datetime(start, errors="coerce") if start is not None else None
    e = pd.to_datetime(end, errors="coerce") if end is not None else None
    mask = pd.Series(True, index=df.index)
    if s is not None:
        mask &= df["TIME_DT"] >= s
    if e is not None:
        mask &= df["TIME_DT"] <= e
    return df[mask]