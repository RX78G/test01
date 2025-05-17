import json
import pathlib
import tkinter as tk
from tkinter import ttk

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

CACHE_DIR = pathlib.Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

INDICATORS = {
    "GDP": "NY.GDP.MKTP.CD",
    "CO2": "EN.ATM.CO2E.PC",
}

def get_indicator_data(country, indicator, cache_dir=CACHE_DIR):
    """Return DataFrame of indicator data for the given country."""
    fname = cache_dir / f"{country}_{indicator}.csv"
    if fname.exists():
        df = pd.read_csv(fname)
    else:
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1000"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()[1]
        df = pd.DataFrame(data)[["date", "value"]]
        df.to_csv(fname, index=False)
    df = df.dropna()
    df["date"] = df["date"].astype(int)
    return df.sort_values("date")


class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("World Bank Dashboard")
        self.country_var = tk.StringVar(value="JPN")
        self.indicator_var = tk.StringVar(value="GDP")
        self.chart_type = tk.StringVar(value="line")
        self._create_widgets()
        self._create_plot()

    def _create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(frm, text="Country code").pack(side=tk.LEFT)
        ttk.Entry(frm, textvariable=self.country_var, width=6).pack(side=tk.LEFT)
        ttk.Label(frm, text="Indicator").pack(side=tk.LEFT)
        ttk.Combobox(frm, textvariable=self.indicator_var, values=list(INDICATORS.keys()), width=5).pack(side=tk.LEFT)
        ttk.Radiobutton(frm, text="Line", variable=self.chart_type, value="line", command=self.update_plot).pack(side=tk.LEFT)
        ttk.Radiobutton(frm, text="Scatter", variable=self.chart_type, value="scatter", command=self.update_plot).pack(side=tk.LEFT)
        ttk.Button(frm, text="Plot", command=self.update_plot).pack(side=tk.LEFT)

    def _create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_plot()

    def update_plot(self):
        code = self.country_var.get()
        ind_key = self.indicator_var.get()
        indicator = INDICATORS[ind_key]
        df = get_indicator_data(code, indicator)
        self.ax.clear()
        if self.chart_type.get() == "line":
            self.ax.plot(df["date"], df["value"], marker="o")
        else:
            self.ax.scatter(df["date"], df["value"])
        self.ax.set_title(f"{code} {ind_key}")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel(ind_key)
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    Dashboard().mainloop()
