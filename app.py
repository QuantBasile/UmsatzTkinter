#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:33:03 2025

@author: fran
"""

# app.py (solo mostrar los puntos donde actualizamos)
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from data.loader import read_all_csvs
from data.filters import filter_by_issuers, filter_by_time
from ui.main_window import MainWindow

FOLDER = r"/home/fran/Desktop/Stamm/"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trading App")
        self.geometry("1100x700")
        self.df_all: pd.DataFrame | None = None
        self.df_view: pd.DataFrame | None = None

        self.main = MainWindow(
            master=self,
            issuers=[],
            on_apply_filters=self.on_apply_filters,
            on_load_data=self.on_load_data
        )

    def _refresh_charts(self):
        self.main.volume_chart.update(self.df_view)
        self.main.trades_chart.update(self.df_view)   # <- NUEVO

    def on_load_data(self):
        try:
            df, errors = read_all_csvs(FOLDER)
            self.df_all = df
            self.df_view = df
            if errors:
                for e in errors[:5]: print("WARN:", e)
            messagebox.showinfo("OK", f"Loaded {len(df):,} rows")

            issuers = sorted(df["ISSUER"].dropna().astype(str).unique().tolist())
            self.main.destroy()
            self.main = MainWindow(
                master=self,
                issuers=issuers,
                on_apply_filters=self.on_apply_filters,
                on_load_data=self.on_load_data
            )
            self._refresh_charts()   # <- refresca ambos
        except Exception as e:
            messagebox.showerror("Load error", str(e))

    def on_apply_filters(self, selected_issuers: list[str], date_from: str | None, date_to: str | None):
        if self.df_all is None:
            messagebox.showwarning("No data", "Load data first.")
            return
        df = filter_by_issuers(self.df_all, selected_issuers)
        df = filter_by_time(df, date_from, date_to)
        self.df_view = df
        self._refresh_charts()       # <- refresca ambos

if __name__ == "__main__":
    App().mainloop()
