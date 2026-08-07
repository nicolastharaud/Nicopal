# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 12:27:02 2026
@author: Nicolas Tharaud
          __  
    ___  |_|____ ___
  / __ \/ / ___/ __ \
 / / / / / |__| |_| |
/_/ /_/_/\___/\____/T
"""

from importlib.resources import files
from matplotlib import font_manager
import matplotlib.pyplot as plt

_registered = False

def use_nunito():
    global _registered

    if not _registered:
        fonts_dir = files("nicopal").joinpath("fonts")

        for font in fonts_dir.iterdir():
            if font.suffix == ".ttf":
                font_manager.fontManager.addfont(str(font))

        _registered = True

    return plt.rc_context({"font.family": "Nunito"})