# Nicopal

## Context
**Nicopal** provides perceptually uniform and colour-vision-deficiency-friendly colour palettes for scientific data visualisation. Inspired by the work of **Fabio Crameri** [1], these palettes are designed to represent data as faithfully as possible, ensuring consistent interpretation across all observers, regardless of their colour vision. Their design follows the perceptual uniformity guidelines of **Peter Kovesi** [2] and uses the colour-vision deficiency simulation model of **Machado et al.** [3]. They are also part of the broader effort, initiated as early as 2004 by **Light & Bartlein** [4], to move away from rainbow-type colourmaps, which are known to introduce perceptual artefacts and mislead interpretation.

These palettes can be used as a drop-in complement to the [colour-vision deficiencies](https://matplotlib.org/stable/users/explain/colors/colormaps.html#color-vision-deficiencies) section of Matplotlib. For more context on colourmap best practices, see the [colourmap selection flowchart](https://s-ink.org/colour-map-guideline) and the [Matplotlib colormaps documentation](https://matplotlib.org/stable/users/explain/colors/colormaps.html).

*Developed by a protanope (red colour deficiency) student, for everyone.*

---

# I. Installation

In a Python console or terminal :

`pip install nicopal`

---

# II. Usage

### 0. Loading the package

`import nicopal as ncp`

---

### 1. Display the package version

`print(ncp.version)`

Displays the version and a short description of the package.

---

### 2. Quickly test all palettes

`ncp.pal_test()`

Checks that all palettes load correctly and displays a confirmation message if everything is valid.

---

### 3. List available palettes

`ncp.pal_list()`

Returns a sorted list of all available palette names.

---

### 4. Visualize a palette

`ncp.pal_show("Lithium")`

Displays a gradient of the chosen palette.
`pal_show` can be used with any palette from `pal_list()`.

---

### 5. Visualiser toutes les palettes

`ncp.pal_all()`

Displays all palettes and their associated names.

---

### 6. Load a palette as a list of HEX colours

`ncp.pal_hex("Lithium")         # all stored colours`
`ncp.pal_hex("Lithium", N=10)   # resample to exactly 10 colours`

Returns the palette as a list of HEX color codes (e.g. `['#1a2b3c', ...]`).
See the [Matplotlib colour formats documentation](https://matplotlib.org/stable/users/explain/colors/colors.html#color-formats) for details on how to use these strings.

---

### 7. Use a palette as a colormap

`colormap   = ncp.pal("Lithium")                 # normal order`               
`colormap_r = ncp.pal("Lithium", reverse=True)   # reversed via parameter`  
`colormap_r = ncp.pal("Lithium_r")               # reversed via '_r' suffix`   
`colormap_r = ncp.pal("Lithium_r").reversed()    # reversed via Matplotlib native method`    

`ax.contourf(x, y, z, cmap = colormap)`

> Palette names are **case-insensitive**: `"lithium"`, `"Lithium"` and `"LITHIUM"` all work.  
> `ax.contourf` can be replaced by any other Matplotlib function that accepts a colormap.  
> `x`, `y` and `z` are your data to visualise.

For more information on reversing and manipulating colormaps, see the [Matplotlib colormap manipulation guide](https://matplotlib.org/stable/users/explain/colors/colormap-manipulation.html#reversing-a-colormap).

---

### 8. Extract colors from a palette

`sample = ncp.pal_sample("Carbon", 6)`   
`x = ["A", "B", "C", "D", "E", "F"]`   
`y = [3, 7, 5, 6, 4, 8]`   
`plt.bar(x, y, color = sample)`   
`plt.show()`   

Returns `n` discrete colors extracted evenly from the palette.

---

### 9. Palette demonstration

`ncp.pal_demo("Selenium")`

Displays example visualizations using the chosen palette : continuous band, 1-D signal, perceptual lightness curve, 2-D field, discrete levels, and colour-vision-deficiency simulation.

---

### 10. Palette names

`Boron` | `Carbon` | `Cesium` | `Chlorine` | `Cobalt` | `Iodine` | `Iridium` | `Iron` | `Lithium` | `Magnesium` | `Manganese` | `Mercury` | `Neon` | `Nickel` | `Nitrogen` | `Osmium` | `Oxygen` | `Radium` | `Rubidium` | `Selenium` | `Silicon` | `Silver` | `Sodium` | `Sulfur` | `Uranium` | `Vanadium` | `Zinc` |

> All names are case-insensitive. The `_r` suffix reverses any palette (e.g. `"Lithium_r"`).

---

# III. Methodology 

Documentation in progress...

***************************************************************** 
#### Bibliography : 

[1] Crameri, F., Shephard, G.E. & Heron, P.J. 2020. 'The Misuse of Colour in Science Communication'.
Nature Communications 11(1): 5444. doi:10.1038/s41467-020-19160-7. 
[Paper link](https://www.nature.com/articles/s41467-020-19160-7)

[2] Kovesi, P. 2015. 'Good Colour Maps: How to Design Them'.
arXiv:1509.03700. 
[Paper link](https://arxiv.org/abs/1509.03700)

[3] Machado, G.M., Oliveira, M.M. & Fernandes, L.A.F. 2009. 'A Physiologically-based Model for Simulation of Color Vision Deficiency'.
IEEE Transactions on Visualization and Computer Graphics 15(6): 1291–1298. doi:10.1109/TVCG.2009.113. 
[Paper link](https://ieeexplore.ieee.org/document/5290741)

[4] Light, A., and P. J.Bartlein (2004), The end of the rainbow? Color schemes for improved data graphics, Eos Trans. 
AGU, 85(40), 385–391, doi:10.1029/2004EO400002. 
[Paper link](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2004EO400002)


*****************************************************************

# :) NT

---
