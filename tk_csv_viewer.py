#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 14:46:50 2025

@author: fran
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# ==== EDITA AQUÍ TU CARPETA CON CSVs ====
FOLDER = r"/home/fran/Desktop/Stamm/"   # <-- pon tu carpeta aquí (puede ser relativa o absoluta)

# ==== Opciones de lectura (ajústalas si hace falta) ====
CSV_EXT = ".csv"
CSV_READ_KW = dict(
    sep=";",          # cambia a "," si tus CSV usan coma
    quotechar='"',
    on_bad_lines="skip",
    dtype=str,        # todo como texto por simplicidad
    engine="python"
)
MAX_ROWS_SHOW = 5_000  # límite para la vista

def read_all_csvs(folder: str) -> pd.DataFrame:
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

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer (mínimo)")
        self.geometry("1100x650")

        top = ttk.Frame(self, padding=6)
        top.pack(fill="x")
        self.status = ttk.Label(top, text="Cargando…")
        self.status.pack(side="left")

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=6, pady=6)

        self.tree = ttk.Treeview(frame, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")

        # carga inmediata al iniciar
        self.after(100, self.load_data)

    def set_table(self, df: pd.DataFrame):
        # limpiar columnas/filas actuales
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
        self.tree.delete(*self.tree.get_children())

        if df.empty:
            self.tree["columns"] = ()
            self.status.config(text="0 filas")
            return

        view_df = df.head(MAX_ROWS_SHOW)
        cols = list(view_df.columns)
        self.tree["columns"] = cols

        for c in cols:
            self.tree.heading(c, text=c)
            # ancho aproximado según longitud media
            width = min(max(80, int(view_df[c].astype(str).str.len().mean() * 9)), 300)
            self.tree.column(c, width=width)

        for row in view_df.itertuples(index=False, name=None):
            self.tree.insert("", "end", values=row)

        info = f"{len(df):,} filas × {len(df.columns)} columnas"
        if len(df) > len(view_df):
            info += f" (mostrando {len(view_df):,})"
        self.status.config(text=info)

    def load_data(self):
        try:
            df, errors = read_all_csvs(FOLDER)
            self.set_table(df)
            if errors:
                messagebox.showinfo(
                    "Avisos de lectura",
                    f"Leídos con éxito. {len(errors)} archivo(s) con problemas (máx 5):\n\n" +
                    "\n".join(errors[:5])
                )
        except Exception as e:
            self.status.config(text="Error")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()
