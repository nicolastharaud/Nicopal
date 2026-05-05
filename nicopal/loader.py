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
from .exceptions import PaletteNotFoundError


def _normalize_name(name):
    stripped = name.strip()
    if stripped.lower().endswith("_r"):
        stripped = stripped[:-2]
    return stripped


def find_file(palette_name, suffix):
    needle = palette_name.lower()
    files = pkg_resources.contents("nicopal.data")
    for f in files:
        if needle in f.lower() and f.endswith(suffix):
            return f
    raise PaletteNotFoundError(
        f"Palette '{palette_name}' not found. "
        "Use ncp.pal_list() to see available palettes.")


def load_hex(name):
    clean = _normalize_name(name)
    filename = find_file(clean, "_hex.json")
    with pkg_resources.open_text("nicopal.data", filename) as f:
        return json.load(f)


def load_rgb(name):
    clean = _normalize_name(name)
    filename = find_file(clean, "_rgb.json")
    with pkg_resources.open_text("nicopal.data", filename) as f:
        return json.load(f)


_CACHE = {}


def load_cmap(name):
    clean = _normalize_name(name)
    if clean in _CACHE:
        return _CACHE[clean]
    filename = find_file(clean, "_cmap.pkl")
    with pkg_resources.open_binary("nicopal.data", filename) as f:
        cmap = pickle.load(f)
    _CACHE[clean] = cmap
    return cmap

    
    