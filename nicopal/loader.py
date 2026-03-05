# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:34:46 2026
@author: Nicolas Tharaud
          __  
    ___  |_|____ ___
  / __ \/ / ___/ __ \
 / / / / / |__| |_| |
/_/ /_/_/\___/\____/T
"""

import json
import pickle
import importlib.resources as pkg_resources

def find_file(palette_name, suffix):
    files = pkg_resources.contents("nicopal.data")
    for f in files:
        if palette_name in f and f.endswith(suffix):
            return f
    raise FileNotFoundError(f"Palette {palette_name} not found")


def load_hex(name):
    filename = find_file(name, "_hex.json")
    with pkg_resources.open_text("nicopal.data", filename) as f:
        return json.load(f)


def load_rgb(name):
    filename = find_file(name, "_rgb.json")
    with pkg_resources.open_text("nicopal.data", filename) as f:
        return json.load(f)


def load_cmap(name):
    filename = find_file(name, "_cmap.pkl")
    with pkg_resources.open_binary("nicopal.data", filename) as f:
        return pickle.load(f)
    
    