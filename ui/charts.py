#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:47:10 2025

@author: fran
"""

# ui/main_window.py
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class BaseChart:
    def __init__(self, parent):
        # parent es el "master": un Frame donde insertamos el canvas
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update(self, df):
        raise NotImplementedError
        
class VolumeChart(BaseChart):
    def update(self, df):
        self.ax.clear()
        if df is None or df.empty or "ISSUER" not in df or "VOLUME" not in df:
            self.ax.set_title("Sin datos")
        else:
            s = df.groupby("ISSUER")["VOLUME"].sum()
            x = s.index.values
            y = s.values
            self.ax.bar(x, y)
            self.ax.set_title("Volumen por día")
            self.ax.set_xlabel("Fecha")
            self.ax.set_ylabel("Volumen")
            self.fig.autofmt_xdate()
        self.canvas.draw_idle()
        

class TradesCountChart:
    def __init__(self, master, top_n: int = 20):
        self.top_n = top_n
        self.fig = Figure(figsize=(6, 3.6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update(self, df: pd.DataFrame):
        self.ax.clear()
        if df is None or df.empty or "ISSUER" not in df or "TIME" not in df:
            self.ax.set_title("No data")
        else:
            # Conteo de trades por emisor
            counts = (df.dropna(subset=["ISSUER"])
                        .groupby("ISSUER")["TIME"]
                        .count()
                        .sort_values(ascending=False))

            # Opcional: limitar a top_n y agrupar el resto como "Others"
            if self.top_n and len(counts) > self.top_n:
                top = counts.iloc[:self.top_n]
                others_sum = counts.iloc[self.top_n:].sum()
                counts = pd.concat([top, pd.Series({"Others": others_sum})])


            self.ax.bar(counts.index.astype(str), counts.values)
            self.ax.set_title("Trades por ISSUER")
            self.ax.set_xlabel("ISSUER")
            self.ax.set_ylabel("Nº trades")

            # ticks legibles
            labels = counts.index.astype(str).tolist()
            if len(labels) > 15:
                step = max(1, len(labels) // 15)
                self.ax.set_xticks(range(0, len(labels), step))
                self.ax.set_xticklabels(labels[::step], rotation=45, ha="right")
            else:
                self.ax.set_xticklabels(labels, rotation=45, ha="right")

        self.fig.tight_layout()
        self.canvas.draw_idle()