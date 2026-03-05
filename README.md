# Nicopal

Ces palettes de couleurs ont été créées par Nicolas Tharaud en s’inspirant de la méthode de Fabio Crameri [1]. Elles ont 
pour but de représenter des variables climatiques de la façon la plus juste possible sans sur ou sous interprétation visuelle. 
Une palette de couleur doit être judicieusement choisie en fonction de la variable à représenter afin que celle-ci soit 
interprétée de la même manière par chaque observateur. Les palettes de couleurs ont été créées par un daltonien 
protanope (déficience couleur rouge). Par ailleurs, le contraste de certaines palettes sera plus visible pour un daltonien 
protanope, que pour une personne possédant une vision « normale » ou bien ayant un autre type de daltonisme. 

---

Les tests ci-dessous ont permis d’évaluer les différentes palettes de couleurs, voici l’explication des tests : 

### Le test de luminosité L*

Le test de luminosité L* examine la variation de la composante L* (0 = noir, 100 = blanc) le long de la palette. Il permet 
de vérifier que la progression de la clarté est harmonieuse, assurant que les nuances de couleur restent perceptibles. 

### Le test de ΔE cumulatif

Le test de ΔE cumulatif mesure la différence perceptuelle entre couleurs consécutives selon la formule CIEDE2000 
(voir Methods dans [1]). La somme cumulée de ces différences fournit un aperçu global de la perceptibilité : une courbe 
régulière indique des transitions uniformes, tandis que des sauts abrupts signalent des changements trop marqués.
 
### Les valeurs de ΔE moyen et ΔE maximal

Les valeurs de ΔE moyen et ΔE maximal résument quantitativement la palette. Le ΔE moyen indique la différence 
perceptuelle moyenne entre couleurs adjacentes, reflétant la régularité globale, tandis que le ΔE maximal correspond à 
la transition la plus prononcée (voir Table 1 dans [2]).


***************************************************************** 
Bibliographie : 

[1] Crameri, Fabio, Grace E. Shephard, and Philip J. Heron. 2020. ‘The Misuse of Colour in Science Communication’. 
Nature Communications 11(1): 5444. doi:10.1038/s41467-020-19160-7. 

[2] Yang, Yang, Jun Ming, and Nenghai Yu. 2012. ‘Color Image Quality Assessment Based on CIEDE2000’. Advances 
in Multimedia 2012: 1–6. doi:10.1155/2012/273723. 
*****************************************************************

## Installation

Dans une console ou un terminal Python :

pip install nicopal

---

## Utilisation

### Chargement de la librairie

import nicopal as ncp

### Voir le nom des palettes disponibles

print(ncp.pal_list())

### Visualiser une palette

ncp.pal_show("nom de la palette")

### Charger une palette en liste HEX

colors = ncp.pal("Lithium")  
print(colors)

### Utiliser les palettes comme colormap

colormap   = ncp.cmap("nom de la palette")  
colormap_r = ncp.cmap("nom de la palette", reverse=True)  
ax.contourf(x, y, z, cmap=colormap)

> reverse = True permet d’inverser la colormap.  
> ax.contourf peut être remplacé par d'autres fonctions de visualisations.  
> x, y, et z sont à remplacer par les variables à visualiser.

---

## Nom des palettes

Boron   | Carbon    | Chlorine  |
Cobalt  | Iodine    | Iron      |
Lithium | Magnesium | Manganese |
Oxygen  | Selenium  | Sodium    |
Sulfur  | Vanadium  |           

# :) NT

---
