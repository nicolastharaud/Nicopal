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
from .font import use_nunito
from .loader import load_hex, load_rgb, _normalize_name
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import importlib.resources as pkg_resources
from matplotlib.colors import LinearSegmentedColormap
from itertools import combinations
from skimage import color as _skcolor

# --- For reverse name
def _parse_name(name):
    stripped = name.strip()
    if stripped.lower().endswith("_r"):
        return stripped[:-2], True
    return stripped, False


# --- For building colormap
def _build_cmap(name, N=256, reverse=False):
    base_name, auto_reverse = _parse_name(name)
    colors = load_hex(base_name)
    if reverse or auto_reverse:
        colors = colors[::-1]
    display_name = _normalize_name(base_name)
    return LinearSegmentedColormap.from_list(display_name, colors, N=N)


# --- Palette as a list of HEX colors
def pal_hex(name, N=None):
    base_name, reverse = _parse_name(name)
    colors = load_hex(base_name)
    if reverse:
        colors = colors[::-1]
    if N is not None:
        cmap = LinearSegmentedColormap.from_list(base_name, colors, N=N)
        return [mcolors.to_hex(cmap(i / (N - 1))) for i in range(N)]
    return colors


# --- Palette as a matplotlib colormap
def pal(name, N=256, reverse=False):
    return _build_cmap(name, N=N, reverse=reverse)


# --- List of Nicopal available
def pal_list():
    files = pkg_resources.contents("nicopal.data")
    palettes = set()
    for f in files:
        if f.endswith("_hex.json"):
            # file names follow the pattern  NNN_PaletteName_hex.json
            name = f.split("_", 1)[1].removesuffix("_hex.json")
            palettes.add(name)
    return sorted(list(palettes))


# --- Visualize a palette
def pal_show(name, N=256):

    with use_nunito():

        colmap = _build_cmap(name, N=N)
        base_name, _ = _parse_name(name)

        gradient = np.linspace(0, 1, N).reshape(1, -1)
        discrete = np.arange(8).reshape(1, -1)

        fig, ax = plt.subplots(figsize=(8, 3))

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(0.5, 0.8, base_name, ha="center", va="center", fontsize=40, fontweight="bold")

        x0     = 0.05
        y0     = 0.08
        width  = 0.90
        height = 0.55

        clip = FancyBboxPatch((x0, y0), width, height, boxstyle="round,pad=0.00,rounding_size=0.04", 
                              lw=0, facecolor="none", transform=ax.transAxes)
        ax.add_patch(clip)
        im1 = ax.imshow(gradient, cmap=colmap, aspect="auto", extent=[ x0, x0 + width, y0 + height / 2, y0 + height],
                        interpolation="bicubic", transform=ax.transAxes, zorder=1)
        im1.set_clip_path(clip)
        im2 = ax.imshow(discrete, cmap=colmap, aspect="auto", extent=[x0, x0 + width, y0, y0 + height / 2], 
                        interpolation="nearest", transform=ax.transAxes, zorder=1)
        im2.set_clim(0, 7)
        im2.set_clip_path(clip)

        for i in range(1, 8):
            x = x0 + width * i / 8
            ax.plot([x, x], [y0, y0 + height / 2], color="white", lw=0, transform=ax.transAxes, zorder=2)

        plt.tight_layout()
        plt.show()

# --- Visualize all palettes
def pal_gallery(N=256, ncols=3, n_discrete=8, reverse=False):
    with use_nunito():
        palettes = pal_list()
        n     = len(palettes)
        nrows = int(np.ceil(n / ncols))
        BG       = "#F8F7F4"
        X0, X1   = 0.06, 0.94
        BW       = X1 - X0
        Y_DISC   = 0.34
        BAND_H   = 0.225
        Y_CONT   = Y_DISC + BAND_H
        gradient  = np.linspace(0, 1, N).reshape(1, -1)
    
        fig = plt.figure(figsize=(2.8 * ncols, 1.50 * nrows), facecolor=BG)
        for idx, name in enumerate(palettes):
            ax = fig.add_subplot(nrows, ncols, idx + 1)
            ax.set_facecolor(BG)
            for sp in ax.spines.values():
                sp.set_visible(False)
            ax.set_xticks([]); ax.set_yticks([])
            cmap = _build_cmap(name, N=N, reverse=reverse)
            clip = FancyBboxPatch((X0, Y_DISC), BW, 2 * BAND_H, boxstyle="round,pad=0,rounding_size=0.03", lw=0, 
                                  facecolor="none", transform=ax.transAxes)
            ax.add_patch(clip)
            bax = ax.inset_axes([X0, Y_CONT, BW, BAND_H])
            im = bax.imshow(gradient, aspect="auto", cmap=cmap)
            im.set_clip_path(clip)
            bax.set_axis_off()
            bounds  = np.linspace(0, 1, n_discrete + 1)
            norm    = mcolors.BoundaryNorm(bounds, cmap.N)
            centers = 0.5 * (bounds[:-1] + bounds[1:])
            disc_img = np.array([[cmap(norm(v))[:3] for v in centers]])
            dax = ax.inset_axes([X0, Y_DISC, BW, BAND_H])
            im = dax.imshow(disc_img, aspect="auto", interpolation="nearest")
            im.set_clip_path(clip)
            dax.set_axis_off()
            ax.text(0.5, 0.16, name, transform=ax.transAxes, ha="center",
                    va="center", fontsize=20, fontweight="bold",
                    color="#3A3835")
        for idx in range(n, nrows * ncols):
            fig.add_subplot(nrows, ncols, idx + 1).set_visible(False)
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01,
                            hspace=0.20, wspace=0.10)
        plt.show()


def pal_all():
    pal_gallery()


# --- Palette valid
def pal_test():
    for p in pal_list():
        assert len(pal_hex(p)) > 0, f"Palette {p} is empty"
    print("All palettes are valid!")


# --- Return n discrete colors
def pal_sample(name, n, reverse=False):
    colmap = _build_cmap(name, N=n, reverse=reverse)
    return [colmap(i / (n - 1)) for i in range(n)]


# --- Show a demonstration of a few figures using the palette
def pal_demo(name):

    with use_nunito():

        CMAP = _build_cmap(name)
        base_name, _ = _parse_name(name)

        SPINEWIDTH = 3
        EDGECOLOR = "black"

        def style_axes(ax):
            ax.tick_params(axis="both", labelsize=0, width=0, length=0)
            for spine in ax.spines.values():
                spine.set_linewidth(SPINEWIDTH)
                spine.set_edgecolor(EDGECOLOR)

        fig = plt.figure(figsize=(15,10), constrained_layout=True)
        gs = fig.add_gridspec(3,3)

        fig.suptitle(base_name, fontsize=30, fontweight="bold")
        
        # --- Scatter
        ax = fig.add_subplot(gs[0,0])
        rng = np.random.RandomState(0)      
        x = rng.uniform(0,1,500)
        y = 5*x + rng.normal(0,2,500)
        x += rng.uniform(-0.2,0.2,500)      
        ax.scatter(x,y,c=y,cmap=CMAP,s=150,ec="black",lw=1.5)     
        style_axes(ax)
        #ax.set_title("Scatter",fontsize=16,fontweight="bold")
        
        # --- Heatmap
        ax = fig.add_subplot(gs[0,1])
        np.random.seed(2)
        data = np.random.random((10,10))
        ax.imshow(data,cmap=CMAP)
        style_axes(ax)
        #ax.set_title("Heatmap",fontsize=16,fontweight="bold")       
        
        # --- Contour
        ax = fig.add_subplot(gs[0,2])
        x = np.linspace(-3,3,200)
        y = np.linspace(-3,3,200)
        X,Y = np.meshgrid(x,y)
        Z = np.sin(X**2+Y**2)/(X**2+Y**2+0.1)
        ax.contourf(X,Y,Z,levels=20,cmap=CMAP)
        style_axes(ax)
        #ax.set_title("Contour",fontsize=16,fontweight="bold")   
        
        # --- Hexbin
        ax = fig.add_subplot(gs[1,0])
        np.random.seed(8)
        x = np.random.normal(0,1,150000)
        y = 3*x + 5*np.random.normal(0,1,150000)
        ax.hexbin(x,y,gridsize=20,bins="log",cmap=CMAP)
        style_axes(ax)
        #ax.set_title("Hexbin",fontsize=16,fontweight="bold")
        
        # --- 3D plot
        ax = fig.add_subplot(gs[1,1],projection="3d")
        X,Y = np.meshgrid(np.linspace(-8,8,100),np.linspace(-8,8,100))
        R = np.sqrt(X**2+Y**2)
        Z = np.sin(R)/R
        ax.plot_surface(X,Y,Z,cmap=CMAP)
        ax.set_axis_off()
        ax.set_box_aspect(None,zoom=1.4)
        #ax.set_title("Surface",fontsize=16,fontweight="bold")
        
        # --- Image
        ax = fig.add_subplot(gs[1,2])
        x = np.linspace(-2,2,250)
        y = np.linspace(-2,2,250)
        X,Y = np.meshgrid(x,y)
        img = np.sin(5*X)*np.cos(4*Y)
        ax.imshow(img,cmap=CMAP,origin="lower")
        style_axes(ax)
        #ax.set_title("Image",fontsize=16,fontweight="bold")
        
        # --- Lineplot
        ax = fig.add_subplot(gs[2,0])
        years = np.arange(2000,2031)
        colors = plt.get_cmap(CMAP)(np.linspace(.1,.9,5))
        for i,color in enumerate(colors):
            values = 60 + np.cumsum(np.random.normal(0.8+i*0.15,1.5,len(years)))
            ax.plot(years,values,lw=5,color=color)
        style_axes(ax)
        #ax.set_title("Line",fontsize=16,fontweight="bold")
        
        # --- Barplot
        ax = fig.add_subplot(gs[2,1])
        values = np.random.uniform(5,30,8)
        colors = plt.get_cmap(CMAP)(np.linspace(.1,.9,8))
        ax.bar(np.arange(8),values,color=colors,ec="black",lw=2)
        style_axes(ax)
        #ax.set_title("Bar",fontsize=16,fontweight="bold")
        
        # --- Palette
        ax = fig.add_subplot(gs[2,2])
        gradient = np.linspace(0,1,256).reshape(1,-1)
        ax.imshow(gradient,aspect="auto",cmap=CMAP)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(3)
        #ax.set_title("Palette",fontsize=16,fontweight="bold")
        plt.show()

# --- Show the same demo but with different graphs which needed the optional dependencies
def pal_demo_advanced(name):

    try:
        
        import matplotlib.patheffects as pe

        from matplotlib.lines import Line2D
        from matplotlib.colors import ListedColormap, BoundaryNorm

        from scipy.ndimage import gaussian_filter

        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        import cartopy.io.shapereader as shpreader

    except ImportError as e:

        raise ImportError(
            "\npal_demo_advanced() requires the optional Nicopal dependencies.\n\n"
            "Install them with:\n\n"
            "pip install 'nicopal[advanced]'\n") from e

    with use_nunito():
        CMAP = _build_cmap(name)
        base_name, _ = _parse_name(name)
        FIGSIZE = (15,10)
        SPINEWIDTH = 3
        EDGECOLOR = "black"

        def style_axes(ax):
            ax.tick_params(axis="both",labelsize=0,width=0,length=0)
            for spine in ax.spines.values():
                spine.set_linewidth(SPINEWIDTH)
                spine.set_edgecolor(EDGECOLOR)
                
        # --- Hexbin        
        def plot_hexbin(ax):
            np.random.seed(8)
            x = np.random.normal(0,1,1_000_000)
            y = 3*x + 5*np.random.normal(0,1,1_000_000)
            ax.hexbin(x,y,gridsize=15,bins="log",cmap=CMAP)
            style_axes(ax)
        
        # --- Heatmap
        def plot_heatmap(ax):
            np.random.seed(2)
            data = np.random.random((8,8))
            ax.imshow(data,cmap=CMAP)
            ax.set_xticks([])
            ax.set_yticks([])
            style_axes(ax)
         
        # --- Ridgeline    
        def plot_ridgeline(ax):
            np.random.seed(5)
            groups = ["Ash","Elm","Fir","Oak","Pine"]
            cmap = plt.get_cmap(CMAP)
            colors = cmap(np.linspace(.15,.9,len(groups)))
            x = np.linspace(-100,600,400)
            offset = 0
            for color,group in zip(colors,groups):
                mu = np.random.uniform(150,350)
                sigma = np.random.uniform(40,90)
                y = np.exp(-(x-mu)**2/(2*sigma**2))
                y /= y.max()
                ax.fill_between(x,offset,y+offset,color=color,ec="black",lw=2)
                offset += 1
            ax.set_xlim(-50,550)
            ax.set_ylim(-0.2,5.2)
            style_axes(ax)
        
        # --- 3D plot    
        def plot_surface(fig,gs):
            ax = fig.add_subplot(gs,projection="3d")
            X,Y = np.meshgrid(np.linspace(-8,8),np.linspace(-8,8))
            R = np.sqrt(X**2+Y**2)
            Z = np.sin(R)/R
            ax.plot_surface(X,Y,Z,cmap=CMAP,alpha=0.9)
            ax.contour(X,Y,Z,colors="black",offset=-1)
            ax.contourf(X,Y,Z,cmap=CMAP,offset=-1,alpha=0.75)
            ax.set(zlim=(-1,0.8))
            ax.set_axis_off()
            ax.set_box_aspect(None,zoom=1.5)
            return ax
        
        # --- Scatter
        def plot_scatter(ax):
            rng = np.random.RandomState(0)
            x = rng.uniform(0,1,500)
            y = 5*x + rng.normal(0,2,500)
            x += rng.uniform(-0.2,0.2,500)
            ax.scatter(x,y,c=y,cmap=CMAP,s=300,ec="black",lw=3)
            style_axes(ax)
            
        # --- Barplot
        def plot_barplot(ax):
            zones = ["Temperate", "Subtropical", "Tropical", "Equatorial"]
            DJF   = [   9.5,          16.0,          22.5,       26.2    ]
            MAM   = [   8.1,          14.9,          22.2,       25.9    ]
            JJA   = [   6.6,          13.5,          21.5,       26.8    ]
            SON   = [   10.4,         13.9,          22.8,       24.8    ]
            cmap   = plt.get_cmap(CMAP)
            colors = cmap(np.linspace(0.10, 0.90, 4))
            x      = np.arange(len(zones))
            w      = 0.20
            ec     = "black"
            lw     = 3
            ax.bar(x-1.5*w, DJF, width=w, color=colors[0], ec=ec, lw=lw)
            ax.bar(x-.5*w,  MAM, width=w, color=colors[1], ec=ec, lw=lw)
            ax.bar(x+.5*w,  JJA, width=w, color=colors[2], ec=ec, lw=lw)
            ax.bar(x+1.5*w, SON, width=w, color=colors[3], ec=ec, lw=lw)
            ax.set_ylim(0,32)
            style_axes(ax)
            
        # --- Lineplot
        def plot_lineplot(ax):
            years = np.arange(2000,2031)
            known = years <= 2025
            future = years >= 2025
            data = {
            "Canada":    np.array([57,60,63,65,66,65,63,61,60,61,64,68,71,73,74,73,72,73,76,80,84,87,89,90,91,92,93,94,95,96,97]),
            "France":    np.array([52,54,57,60,64,67,69,68,66,64,65,69,73,77,80,82,81,80,82,86,90,93,95,96,97,98,100,102,104,106,108]),
            "China":     np.array([61,62,64,67,71,74,76,75,73,71,72,75,79,83,86,88,89,90,92,95,98,100,101,102,103,104,106,108,110,112,114]),
            "Brazil":    np.array([64,66,68,69,68,66,64,63,64,66,69,72,74,75,74,73,72,73,75,78,81,83,84,85,86,87,88,89,90,91,92]),
            "Australia": np.array([69,71,73,75,76,75,73,72,73,75,78,81,84,86,87,86,85,86,88,91,94,96,98,99,100,101,103,105,107,109,111]),
            "India":     np.array([55,57,60,64,68,71,73,72,71,72,75,79,83,87,90,92,93,94,96,99,102,104,106,107,108,109,111,113,115,117,120])}
            uncertainty = {}
            for country, values in data.items():
                unc = np.zeros_like(values)
                unc[years >= 2020] = np.linspace(1,5,np.sum(years >= 2020))
                uncertainty[country] = unc
            cmap = plt.get_cmap(CMAP)
            colors = cmap(np.linspace(.1,.9,len(data)))
            for color,(country,values) in zip(colors,data.items()):
                unc = uncertainty[country]
                ax.fill_between(years,values-unc,values+unc,color=color,alpha=.5)
                ax.plot(years[known],values[known],lw=8,color=color,solid_capstyle="round")
                ax.plot(years[future],values[future],lw=8,color=color,ls=":")
            ax.set_xlim(2000,2030)
            ax.set_ylim(60,120)
            style_axes(ax)
            for line in ax.lines:
                if isinstance(line,Line2D):
                    line.set_path_effects([
                        pe.Stroke(linewidth=line.get_linewidth()+3,foreground="black"),
                        pe.Normal()])
                    
        # --- World Map    
        def tourism_score(country_name):
            rng   = np.random.default_rng(abs(hash(country_name)) % (2**32))
            score = rng.normal(60, 18)
            score = np.clip(score, 5, 95)
            high  = {"France","Italy","Spain","Japan","New Zealand","Greece","Australia","Norway","Iceland","Switzerland","Canada","Brazil",
                     "Thailand","Indonesia","Mexico","Portugal","Peru","Nepal","United States of America","South Africa"}
            low   = {"Greenland","Libya","Niger","Chad","Sudan","South Sudan","Afghanistan","Turkmenistan","Mali"}
            if country_name in high:
                score += 20
            if country_name in low:
                score -= 30
            return np.clip(score,0,100)
        
        def plot_world_map(fig, gs):
            ax = fig.add_subplot(gs, projection=ccrs.Robinson())
            ax.set_global()
            shpfilename = shpreader.natural_earth(resolution="110m", category="cultural", name="admin_0_countries")
            reader = shpreader.Reader(shpfilename)
            records = list(reader.records())
            bounds = np.arange(0,110,10)
            cmap = plt.get_cmap(CMAP)
            cmap_disc = ListedColormap(cmap(np.linspace(0,1,len(bounds)-1)))
            norm = BoundaryNorm(bounds, cmap_disc.N)
            for rec in records:
                country = rec.attributes["NAME_LONG"]
                color   = cmap_disc(norm(tourism_score(country)))
                ax.add_geometries([rec.geometry], crs=ccrs.PlateCarree(), facecolor=color, ec="black", lw=1.5)
            geo = ax.spines["geo"]
            geo.set_linewidth(3)
            geo.set_edgecolor("black")
            style_axes(ax)
            return ax
        
        # --- Ocean Map
        def plot_ocean_map(fig, gs):
            ax = fig.add_subplot(gs, projection=ccrs.Robinson())
            ax.set_global()
            LAND_COLOR = "#d9d9d9"
            lon = np.linspace(-180,180,361); lat = np.linspace(-90,90,181)
            Lon, Lat = np.meshgrid(lon, lat)
        
            def gaussian(lon0, lat0, sx, sy, amp, theta=0):
                th = np.deg2rad(theta)
                dx = (Lon-lon0)*np.cos(th) + (Lat-lat0)*np.sin(th)
                dy = -(Lon-lon0)*np.sin(th) + (Lat-lat0)*np.cos(th)
                return amp * np.exp(-(dx/sx)**2 - (dy/sy)**2)
        
            depth = np.full_like(Lon, 60.0)
        
            for p in [(-45,30,40,18,270,25), (-20,-28,35,18,240,-20), (-155,28,55,18,300,15), (-120,-30,60,20,280,-15), (85,-25,45,18,250,20)]:
                depth += gaussian(*p)
        
            rng = np.random.default_rng(42)
            noise = gaussian_filter(rng.normal(0,1,Lon.shape), sigma=(4,4), mode="wrap")
            noise = (noise - noise.mean()) / noise.std()
            depth += 18 * noise
        
            depth -= 110 * np.exp(-(Lat/11)**2)
            depth -= 120 * (np.abs(Lat)/90)**2
        
            margins = [(-75,0,18,22,140), (-10,5,18,20,150), (20,0,15,20,100), (110,5,25,20,160),
                       (135,35,18,12,120), (-125,35,18,12,120), (-60,-40,20,10,90), (35,-35,18,12,90)]
            for p in margins: depth -= gaussian(*p)
        
            upwellings = [(-80,-15,14,10,150), (12,-22,14,10,150), (-125,35,16,12,120), (-15,25,12,10,100), (55,8,18,10,70)]
            for p in upwellings: depth -= gaussian(*p)
        
            ridge_atl = np.exp(-((Lon + 25*np.sin(np.deg2rad(Lat*3))) / 10)**2)
            ridge_pac = np.exp(-((Lon + 110 + 18*np.sin(np.deg2rad(Lat*2))) / 11)**2)
            ridge_ind = np.exp(-((Lon - 65 + 10*np.sin(np.deg2rad(Lat*2.5))) / 10)**2)
            depth -= 35*ridge_atl; depth -= 28*ridge_pac; depth -= 20*ridge_ind
        
            reefs = [(150,-18,5,4,80), (73,3,3,3,70), (-76,24,5,4,60), (-150,-17,8,6,60), (145,7,6,5,50), 
                     (167,-20,5,5,55), (-90,-1,6,4,40), (55,-5,5,5,45)]
            for p in reefs: depth += gaussian(*p)
        
            depth += 20*np.sin(np.deg2rad(.8*Lon))
            depth += 12*np.sin(np.deg2rad(2*Lon+Lat))
            depth += 10*np.cos(np.deg2rad(3*Lon-2*Lat))
            depth = np.clip(depth,1,500)
        
            bounds    = np.arange(10,400,50)
            cmap_base = plt.get_cmap(CMAP)
            colors    = cmap_base(np.linspace(0,1,len(bounds)+1))
            cmap_disc = ListedColormap(colors[1:-1]); cmap_disc.set_under(colors[0]); cmap_disc.set_over(colors[-1])
            norm      = BoundaryNorm(bounds, cmap_disc.N, clip=False)
            ax.contourf(lon, lat, depth, transform=ccrs.PlateCarree(), levels=bounds, cmap=cmap_disc, norm=norm, extend="both")
            ax.add_feature(cfeature.LAND, facecolor=LAND_COLOR, edgecolor="black", linewidth=2, zorder=20)
            geo       = ax.spines["geo"]; geo.set_visible(True); geo.set_linewidth(3); geo.set_edgecolor("black")
            style_axes(ax)
            return ax
        
        fig = plt.figure(figsize=FIGSIZE,constrained_layout=True)
        gs = fig.add_gridspec(3,3)
        fig.suptitle(f"{base_name} - Advanced demo",fontsize=30,fontweight="bold")
        ax = fig.add_subplot(gs[0,0])
        plot_scatter(ax)
        ax = fig.add_subplot(gs[0,1])
        plot_heatmap(ax)
        ax = fig.add_subplot(gs[0,2])
        plot_ridgeline(ax)
        plot_world_map(fig,gs[1,0])
        ax = fig.add_subplot(gs[1,1])
        plot_hexbin(ax)
        plot_ocean_map(fig,gs[1,2])
        ax = fig.add_subplot(gs[2,0])
        plot_lineplot(ax)
        plot_surface(fig,gs[2,1])
        ax = fig.add_subplot(gs[2,2])
        plot_barplot(ax)
        plt.show()
        
        