# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:43:56 2026
@author: Nicolas Tharaud
          __  
    ___  |_|____ ___
  / __ \/ / ___/ __ \
 / / / / / |__| |_| |
/_/ /_/_/\___/\____/T
"""

from matplotlib.colors import LinearSegmentedColormap
from .loader import load_hex
import importlib.resources as pkg_resources
import numpy as np
import matplotlib.pyplot as plt

# --- Palette as a list of HEX colors
def pal(name):
    return load_hex(name)

# --- Palette as a matplotlib colormap
def cmap(name, N=256):
    colors = load_hex(name)
    return LinearSegmentedColormap.from_list(name, colors, N=N)

# --- List of Nicopal available
def pal_list():
    files = pkg_resources.contents("nicopal.data")
    palettes = set()
    for f in files:
        if f.endswith("_hex.json"):
            name = f.split("_")[1]   
            palettes.add(name)
    return sorted(list(palettes))

# --- Visualize a palette
def pal_show(name, N=256):
    colmap = cmap(name, N)
    gradient = np.linspace(0,1,N).reshape(1,-1)
    plt.figure(figsize=(6,1))
    plt.imshow(gradient, aspect="auto", cmap=colmap)
    plt.axis("off")
    plt.title(name)
    plt.show()