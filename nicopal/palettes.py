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

import numpy as np
from .loader import load_hex
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import importlib.resources as pkg_resources
from matplotlib.colors import LinearSegmentedColormap

# --- Palette as a list of HEX colors
def pal_hex(name):
    return load_hex(name)

# --- Palette as a matplotlib colormap
def pal(name, N=256, reverse=False):
    colors = load_hex(name)
    if reverse:
        colors = colors[::-1]
    return LinearSegmentedColormap.from_list(name, colors, N=N)

# --- List of Nicopal available
def pal_list():
    files = pkg_resources.contents("nicopal.data")
    palettes = set()
    for f in files:
        if f.endswith("_hex.json"):
            name = f.split("_", 1)[1].removesuffix("_hex.json")
            palettes.add(name)
    return sorted(list(palettes))

# --- Visualize a palette
def pal_show(name, N=256):
    colmap = pal(name, N)
    gradient = np.linspace(0,1,N).reshape(1,-1)
    plt.figure(figsize=(6,1))
    plt.imshow(gradient, aspect="auto", cmap=colmap)
    plt.axis("off")
    plt.title(name)
    plt.show()
    
# --- Visualize all palettes
def pal_gallery(N=256, ncols=3, n_discrete=10, reverse=False):
    palettes = pal_list()
    n     = len(palettes)
    nrows = int(np.ceil(n / ncols))
    BG       = "#F8F7F4"
    X0, X1   = 0.06, 0.94          
    BW       = X1 - X0             
    Y_CONT   = 0.56                
    Y_DISC   = 0.34                
    BAND_H   = 0.20                
    GAP      = Y_CONT - (Y_DISC + BAND_H)   
    gradient  = np.linspace(0, 1, N).reshape(1, -1)
    disc_vals = np.linspace(0, 1, n_discrete).reshape(1, -1)

    fig = plt.figure(figsize=(2.8 * ncols, 1.55 * nrows), facecolor=BG)
    for idx, name in enumerate(palettes):
        ax = fig.add_subplot(nrows, ncols, idx + 1)
        ax.set_facecolor(BG)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
        cmap = pal(name, N=N, reverse=reverse)
        bax = ax.inset_axes([X0, Y_CONT, BW, BAND_H])
        bax.imshow(gradient, aspect="auto", cmap=cmap)
        bax.set_axis_off()
        bounds  = np.linspace(0, 1, n_discrete + 1)
        norm    = mcolors.BoundaryNorm(bounds, cmap.N)
        centers = 0.5 * (bounds[:-1] + bounds[1:])
        disc_img = np.array([[cmap(norm(v))[:3] for v in centers]])  
        dax = ax.inset_axes([X0, Y_DISC, BW, BAND_H])
        dax.imshow(disc_img, aspect="auto", interpolation="nearest")
        dax.set_axis_off()
        total_h = BAND_H + GAP + BAND_H
        box = FancyBboxPatch((X0, Y_DISC), BW, total_h, boxstyle="round,pad=0.005,rounding_size=0.035", 
                             transform=ax.transAxes, linewidth=0.7, edgecolor="#CCCAC0", 
                             facecolor="none", zorder=4, clip_on=False)
        ax.add_patch(box)
        ax.text(0.5, 0.16, name, transform=ax.transAxes, ha="center", va="center",
                fontsize=15, fontfamily="monospace", color="#3A3835")
    for idx in range(n, nrows * ncols):
        fig.add_subplot(nrows, ncols, idx + 1).set_visible(False)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99,  bottom=0.01, hspace=0.20, wspace=0.10)
    plt.show()

def pal_all():
    pal_gallery()
    
# --- Palette valid
def pal_test():
    for p in pal_list():
        assert len(pal_hex(p)) > 0, f"Palette {p} empty"
    print("All palettes are valid!")
    
# --- Return n discrete colors
def pal_sample(name, n, reverse=False):
    colmap = pal(name, N=n, reverse=reverse)
    return [colmap(i/(n-1)) for i in range(n)]

# --- Show a demo of color map
def _cmap_colors(cmap, N=256):
    return cmap(np.linspace(0, 1, N))

def _rgb_to_lightness(rgba):
    rgb = rgba[:, :3].clip(0, 1)
    linear = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    Y = linear @ np.array([0.2126, 0.7152, 0.0722])
    eps = 216 / 24389
    L = np.where(Y > eps, 116 * Y ** (1 / 3) - 16, 24389 / 27 * Y)
    return L

_CVD_MATRICES = {
    "deuteranopia": np.array([
        [ 0.29275,  0.70725,  0.00000],
        [ 0.29275,  0.70725,  0.00000],
        [-0.02234,  0.02234,  1.00000]]),
    
    "protanomaly": np.array([
        [ 0.11238,  0.88762,  0.00000],
        [ 0.11238,  0.88762,  0.00000],
        [ 0.00401, -0.00401,  1.00000]]),
    
    "tritanomaly": np.array([
        [ 1.00000,  0.15236, -0.15236],
        [ 0.00000,  0.86717,  0.13283],
        [ 0.00000,  0.86717,  0.13283]])}

def _simulate_cvd(rgba, mode):
    rgb = rgba[:, :3].copy()
    if mode == "grayscale":
        gray = rgb @ np.array([0.2126, 0.7152, 0.0722])
        return np.stack([gray, gray, gray], axis=1)
    return (rgb @ _CVD_MATRICES[mode].T).clip(0, 1)

def _colorbar_image(cmap, N=256):
    return cmap(np.linspace(0, 1, N))[np.newaxis, :]

def _plot_colorbar(ax, cmap, vmin, vmax):
    img = _colorbar_image(cmap)
    ax.imshow(img, aspect="auto", extent=[vmin, vmax, 0, 1])
    ax.set_yticks([])
    ax.set_xlabel("Index", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(10))
    ax.set_title("Continuous band", fontsize=10, fontweight="bold")


def _plot_signal_1d(ax, cmap, vmin, vmax):
    x = np.linspace(0, 4 * np.pi, 500)
    y = np.sin(x) * 25 + 2 * np.cos(2.3 * x)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    ax.scatter(x, y, c=y, cmap=cmap, norm=norm, s=6, linewidths=0)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(vmin - 2, vmax + 2)
    ax.set_xticks([])
    ax.set_ylabel("Index", fontsize=9)
    ax.axhline(0, color="white", lw=0.6, ls="--", alpha=0.7)
    ax.set_title("1-D signal", fontsize=10, fontweight="bold")


def _plot_lightness(ax, cmap, N=256):
    rgba = _cmap_colors(cmap, N)
    L    = _rgb_to_lightness(rgba)
    t    = np.linspace(0, 1, N)
    ax.plot([0, 1], [L[0], L[-1]], color="gray", lw=0.8, ls="--", alpha=0.6, label="linear reference")
    for i in range(N - 1):
        ax.plot(t[i:i+2], L[i:i+2], color=rgba[i, :3], lw=2.5, solid_capstyle="round")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    ax.set_xlabel("normalised value", fontsize=9)
    ax.set_ylabel("L* (CIELAB)", fontsize=9)
    ax.legend(fontsize=7, framealpha=0.4, loc="best")
    ax.set_title("Perceptual lightness", fontsize=10, fontweight="bold")


def _plot_field_2d(ax, cmap, vmin, vmax):
    nlat, nlon = 90, 180
    lat = np.linspace(-90, 90, nlat)
    lon = np.linspace(0, 360, nlon)
    lat2d, lon2d = np.meshgrid(lat, lon, indexing="ij")
    field = 28 * np.cos(np.deg2rad(lat2d)) - 4 * np.sin(np.deg2rad(lon2d))
    norm  = mcolors.Normalize(vmin=vmin, vmax=vmax)
    ax.pcolormesh(lon, lat, field, cmap=cmap, norm=norm, shading="auto")
    ax.set_xlim(0, 360); ax.set_ylim(-90, 90)
    ax.set_xticks(np.arange(0, 361, 90))
    ax.set_yticks(np.arange(-90, 91, 45))
    ax.set_xticklabels(["0°", "90°E", "180°", "90°W", "360°"], fontsize=7)
    ax.set_yticklabels(["-90°", "-45°", "0°", "45°", "90°"], fontsize=7)
    ax.set_title("2-D field", fontsize=10, fontweight="bold")


def _plot_discrete(ax, cmap, vmin, vmax, N=10):
    bounds  = np.linspace(vmin, vmax, N + 1)
    norm    = mcolors.BoundaryNorm(bounds, cmap.N)
    centers = 0.5 * (bounds[:-1] + bounds[1:])
    colors  = [cmap(norm(c)) for c in centers]
    ax.bar(centers, np.ones(N), width=(vmax - vmin) / N * 0.92, color=colors, edgecolor="white", linewidth=0.4)
    ax.set_xlim(vmin, vmax)
    ax.set_ylim(0, 1.15)
    ax.set_yticks([])
    ax.set_xlabel("Index", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(10))
    ax.set_title(f"{N} discrete levels", fontsize=10, fontweight="bold")


def _plot_cvd(ax, cmap, N=256):
    rgba  = _cmap_colors(cmap, N)
    modes = [
        ("Normal",       rgba[:, :3]),
        ("Deuteranopia", _simulate_cvd(rgba, "deuteranopia")),
        ("Protanopia",  _simulate_cvd(rgba, "protanomaly")),
        ("Tritanopia",  _simulate_cvd(rgba, "tritanomaly")),
        ("Grayscale",    _simulate_cvd(rgba, "grayscale"))]
    for i, (label, rgb) in enumerate(modes):
        ax.imshow(rgb[np.newaxis, :], aspect="auto", extent=[0, 1, i, i + 0.85])
        ax.text(-0.02, i + 0.42, label, ha="right", va="center", fontsize=8, transform=ax.get_yaxis_transform())
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(modes))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("CVD simulation", fontsize=10, fontweight="bold")

def pal_demo(name, vmin=-30, vmax=30):
    fig, axes = plt.subplots(2, 3, figsize=(18, 8), gridspec_kw={"hspace": 0.48, "wspace": 0.32},)
    fig.suptitle(f"Nicopal demo: {name}", fontsize=14, fontweight="bold", y=1)

    _plot_colorbar(axes[0, 0], pal(name), vmin, vmax)
    _plot_signal_1d(axes[0, 1], pal(name), vmin, vmax)
    _plot_lightness(axes[0, 2], pal(name))
    _plot_field_2d(axes[1, 0], pal(name), vmin, vmax)
    _plot_discrete(axes[1, 1], pal(name), vmin, vmax)
    _plot_cvd(axes[1, 2], pal(name))
    
    plt.show()