# Nicopal

## Context
**Nicopal** provides perceptually uniform and colour-vision-deficiency-friendly colour palettes for scientific data visualisation. Inspired by the work of **Fabio Crameri** [1], these palettes are designed to represent data as faithfully as possible, ensuring consistent interpretation across all observers — regardless of their colour vision.
Developed by a protanope (red colour deficiency) student, for everyone.

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

Displays the version and a very short description of the package.

---

### 2. Quickly test all palettes

`print(ncp.pal_test())`

Checks that all palettes load correctly.
Displays a confirmation message if everything is valid

---

### 3. List available palettes

`print(ncp.pal_list())`

Displays all available palette names in Nicopal.

---

### 4. Visualize a palette

`print(ncp.pal_show("Lithium"))`

Displays a gradient of the chosen palette.
`pal_show` can be used with any palette from `pal_list()`.

---

### 5. Visualiser toutes les palettes

`print(ncp.pal_all())`

Displays all palettes and their associated names.

---

### 6. Charger une palette en liste HEX

`print(ncp.pal_hex("Lithium"))`

Returns the palette as the corresponding HEX color codes.

---

### 7. Use a palette as a colormap

`colormap   = ncp.pal("Lithium")`               
`colormap_r = ncp.pal("Lithium", reverse=True)`   

`ax.contourf(x, y, z, cmap=colormap)`

> `reverse=True` allows the colormap to be reversed.   
> `ax.contourf` can be replaced by any other Matplotlib function that accepts a colormap.   
> `x`, `y` and `z` are your data to visualize. 

---

### 8. Extract colors from a palette

`sample = ncp.pal_sample("Carbon", 6)`   
`x = ["A","B","C","D","E","F"]`   
`y = [3,7,5,6,4,8]`   
`plt.bar(x, y, color=sample)`   
`plt.show()`   

Returns `n` discrete colors extracted from the palette.

---

### 9. Palette demonstration

`print(ncp.pal_demo("Lithium"))`

Displays example visualizations using the chosen palette

---

### 10. Palette names

`Boron` | `Carbon` | `Cesium` | `Chlorine` | `Cobalt` | `Iodine` | `Iridium` | `Iron` | `Lithium` | `Magnesium` | `Manganese` | `Mercury` | `Neon` | `Nickel` | `Nitrogen` | `Osmium` | `Oxygen` | `Radium` | `Rubidium` | `Selenium` | `Silicon` | `Silver` | `Sodium` | `Sulfur` | `Uranium` | `Vanadium` | `Zinc` |

---

# III. Methodology 

Documentation in progress...

***************************************************************** 
#### Bibliography : 

[1] Crameri, Fabio, Grace E. Shephard, and Philip J. Heron. 2020. ‘The Misuse of Colour in Science Communication’. 
Nature Communications 11(1): 5444. doi:10.1038/s41467-020-19160-7. 

*****************************************************************

# :) NT

---
