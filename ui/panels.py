#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:46:59 2025

@author: fran
"""

# ui/panels/filters_panel.py
import tkinter as tk
from tkinter import ttk
from typing import Callable, Iterable

class FiltersPanel(ttk.Frame):
    """
    Multiselección de Issuers + rango de fechas + botón Apply.
    on_apply(selected_issuers, date_from_str, date_to_str)
    """
    def __init__(self, master, issuers: Iterable[str],
                 on_apply: Callable[[list[str], str | None, str | None], None]):
        super().__init__(master, padding=6)
        self.on_apply = on_apply

        # Issuers
        ttk.Label(self, text="Issuers", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.listbox = tk.Listbox(self, selectmode="extended", exportselection=False, height=12)
        self.listbox.pack(fill="both", expand=True, pady=(4, 8))
        for issuer in sorted({str(x) for x in issuers if x is not None}):
            self.listbox.insert(tk.END, issuer)

        row = ttk.Frame(self); row.pack(fill="x", pady=(0, 8))
        ttk.Button(row, text="Select all", command=lambda: self.listbox.select_set(0, tk.END)).pack(side="left")
        ttk.Button(row, text="Clear", command=lambda: self.listbox.select_clear(0, tk.END)).pack(side="left", padx=6)

        # Date range
        box = ttk.LabelFrame(self, text="Date range")
        box.pack(fill="x", pady=(0, 8))
        frm = ttk.Frame(box); frm.pack(fill="x", padx=4, pady=4)

        ttk.Label(frm, text="From:").grid(row=0, column=0, sticky="w")
        self.ent_from = ttk.Entry(frm, width=16)
        self.ent_from.grid(row=0, column=1, padx=(6, 12))
        ttk.Label(frm, text="(YYYY-MM-DD)").grid(row=0, column=2, sticky="w")

        ttk.Label(frm, text="To:").grid(row=1, column=0, sticky="w")
        self.ent_to = ttk.Entry(frm, width=16)
        self.ent_to.grid(row=1, column=1, padx=(6, 12))
        ttk.Label(frm, text="(YYYY-MM-DD)").grid(row=1, column=2, sticky="w")

        # Apply
        ttk.Button(self, text="Apply", command=self._apply).pack(fill="x")

    def _apply(self):
        idxs = self.listbox.curselection()
        selected = [self.listbox.get(i) for i in idxs]
        date_from = self.ent_from.get().strip() or None
        date_to   = self.ent_to.get().strip() or None
        self.on_apply(selected, date_from, date_to)

