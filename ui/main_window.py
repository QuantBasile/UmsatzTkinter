#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:46:47 2025

@author: fran
"""

# ui/main_window.py (añade lo marcado)
import tkinter as tk
from tkinter import ttk
from ui.panels import FiltersPanel
from ui.charts import VolumeChart
from ui.charts import TradesCountChart   # <- NUEVO

class MainWindow(ttk.Frame):
    def __init__(self, master, issuers, on_apply_filters, on_load_data):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        top = ttk.Frame(self); top.pack(fill="x", padx=8, pady=6)
        ttk.Button(top, text="Load data", command=on_load_data).pack(side="left")

        body = ttk.Frame(self); body.pack(fill="both", expand=True)
        self.filters_panel = FiltersPanel(body, issuers=issuers, on_apply=on_apply_filters)
        self.filters_panel.pack(side="left", fill="y", padx=8, pady=8)

        right = ttk.Frame(body); right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        # contenedores para gráficos
        chart_top = ttk.Frame(right); chart_top.pack(fill="both", expand=True)
        chart_bottom = ttk.Frame(right); chart_bottom.pack(fill="both", expand=True, pady=(8,0))

        self.volume_chart = VolumeChart(chart_top)
        self.trades_chart = TradesCountChart(chart_bottom, top_n=20)  # <- NUEVO
