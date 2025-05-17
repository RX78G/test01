# coding: utf-8
import tkinter as tk
from tkinter import ttk
import math


def cnd(x: float) -> float:
    """Cumulative normal distribution using error function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(S: float, K: float, T: float, r: float, sigma: float, option: str) -> float:
    """Calculate Black-Scholes option price."""
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option == "Call":
        return S * cnd(d1) - K * math.exp(-r * T) * cnd(d2)
    else:
        return K * math.exp(-r * T) * cnd(-d2) - S * cnd(-d1)


n_points = 100


class BlackScholesApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Black-Scholes Simulator")
        self.vars = {
            "S": tk.DoubleVar(value=100.0),
            "K": tk.DoubleVar(value=100.0),
            "r": tk.DoubleVar(value=0.05),
            "sigma": tk.DoubleVar(value=0.2),
            "T": tk.DoubleVar(value=1.0),
            "type": tk.StringVar(value="Call"),
        }
        ctrl = ttk.Frame(root)
        ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self._add_slider(ctrl, "S", 50, 150)
        self._add_slider(ctrl, "K", 50, 150)
        self._add_slider(ctrl, "r", 0.0, 0.1)
        self._add_slider(ctrl, "sigma", 0.05, 0.5)
        self._add_slider(ctrl, "T", 0.1, 2.0)
        ttk.Label(ctrl, text="Type").pack()
        ttk.OptionMenu(ctrl, self.vars["type"], "Call", "Call", "Put", command=lambda _v: self.update()).pack(fill=tk.X)
        self.price_lbl = ttk.Label(ctrl, text="Price: 0.00", font=("Arial", 14))
        self.price_lbl.pack(pady=10)
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        self.update()

    def _add_slider(self, frame: ttk.Frame, name: str, fr: float, to: float) -> None:
        ttk.Label(frame, text=name).pack()
        ttk.Scale(frame, variable=self.vars[name], from_=fr, to=to,
                  command=lambda _e: self.update()).pack(fill=tk.X)
        ttk.Entry(frame, textvariable=self.vars[name], width=7).pack(pady=(0, 5))

    def update(self) -> None:
        S = self.vars["S"].get()
        K = self.vars["K"].get()
        r = self.vars["r"].get()
        sigma = self.vars["sigma"].get()
        T = self.vars["T"].get()
        otype = self.vars["type"].get()
        price = bs_price(S, K, T, r, sigma, otype)
        self.price_lbl.configure(text=f"Price: {price:.2f}")
        self._draw_chart(K, T, r, sigma, otype)

    def _draw_chart(self, K: float, T: float, r: float, sigma: float, otype: str) -> None:
        self.canvas.delete("all")
        width = int(self.canvas["width"])
        height = int(self.canvas["height"])
        s_min = 0.5 * K
        s_max = 1.5 * K
        last_x, last_y = None, None
        for i in range(n_points + 1):
            s = s_min + (s_max - s_min) * i / n_points
            p = bs_price(s, K, T, r, sigma, otype)
            x = int((s - s_min) / (s_max - s_min) * width)
            y = height - int(p / (K * 0.6) * height)
            y = min(max(y, 0), height)
            if last_x is not None:
                self.canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y
        self.canvas.create_line(0, height, width, height, fill="black")
        self.canvas.create_line(0, 0, 0, height, fill="black")


if __name__ == "__main__":
    root = tk.Tk()
    BlackScholesApp(root)
    root.mainloop()
