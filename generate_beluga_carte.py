import folium
import pandas as pd
from adress_utils import AdressUtils
import requests
from folium.plugins import Search
import argparse
import random

COLORS = {
    "blue": "blue",
    "green": "green",
    "red": "red",
    "yellow": "orange",
}

parser = argparse.ArgumentParser(
    description="Generateur de la carte des contacts Beluga, pour faciliter les mises en relation covoiturage."
)
parser.add_argument(
    "--input",
    dest="xls_input_file",
    default="exemple_contacts.xlsx",
    help="Nom du fichier contenant les contacts",
)


parser.add_argument(
    "--output",
    dest="html_output_file",
    default="carte_contacts.html",
    help="Fichier html de sortie contenant la carte",
)

# Analyser les arguments à partir de la ligne de commande
args = parser.parse_args()
print(
    "generation de la carte a partir du fichier source '%s'\nLa carte sera générée dans le fichier '%s'"
    % (args.xls_input_file, args.html_output_file)
)
df = pd.read_excel(args.xls_input_file)
print("")

print("Lecture de %d contacts" % len(df.index))
# Créer une carte centrée sur Montpellier
m = folium.Map(location=[43.6109, 3.8772], zoom_start=11)

# Ajouter un titre à la carte
title_html = '<h3 align="center" style="font-size:20px"><b>Beluga ! </b> les adresses sont floutées, sans numéro de rue</h3>'
m.get_root().html.add_child(folium.Element(title_html))

# creation des layers
lutin_group = folium.FeatureGroup(name="Lutin")
louveteau_group = folium.FeatureGroup(name="Louveteau")
eclai_group = folium.FeatureGroup(name="Eclai.es")
aines_group = folium.FeatureGroup(name="Aines")

m.add_child(lutin_group)
m.add_child(louveteau_group)
m.add_child(eclai_group)
m.add_child(aines_group)

adress_utils = AdressUtils()
# Ajouter des marqueurs pour chaque enfant
for index, row in df.iterrows():
    popup_content = f"<H3>{row['enfant']}</H3> <h4> 0{row['contact']} </h4> <h5>{row['email']} </h5> <p> {row['parent']}</p>"
    icon = None
    if row["groupe"] == "Lutin":
        icon = folium.Icon(color=COLORS["blue"], prefix="fa", icon="hippo")
        if row["parent"] == "Repons":
            icon = folium.Icon(color=COLORS["blue"], prefix="fa", icon="ghost")

    elif row["groupe"] == "Louveteau":
        icon = folium.Icon(color=COLORS["yellow"], prefix="fa", icon="cat")
        if row["parent"] == "Repons":
            icon = folium.Icon(color=COLORS["yellow"], prefix="fa", icon="ghost")
    elif row["groupe"] == "Eclai.es":
        icon = folium.Icon(color=COLORS["green"], prefix="fa", icon="paw")
        if row["parent"] == "Repons":
            icon = folium.Icon(color=COLORS["green"], prefix="fa", icon="ghost")
    elif row["groupe"] == "Aines":
        icon = folium.Icon(color=COLORS["red"], prefix="fa", icon="rocket")
        if row["parent"] == "Repons":
            icon = folium.Icon(color=COLORS["red"], prefix="fa", icon="ghost")
    else:
        icon = folium.Icon(color=COLORS["red"], icon="info-sign")
    marker = folium.Marker(
        location=adress_utils.get_coordinates(
            row["adresse floute"]
        ),  # Vous devez remplacer ces coordonnées par celles de chaque lieu de rencontre
        popup=folium.Popup(popup_content, max_width=300),
        name=popup_content,
        icon=icon,
    ).add_to(m)

    # Ajouter le marqueur au groupe approprié
    if df["groupe"][index] == "Lutin":
        marker.add_to(lutin_group)
    elif df["groupe"][index] == "Louveteau":
        marker.add_to(louveteau_group)
    elif df["groupe"][index] == "Eclai.es":
        marker.add_to(eclai_group)
    elif df["groupe"][index] == "Aines":
        marker.add_to(aines_group)

# ajout du layer control
folium.LayerControl().add_to(m)

# Sauvegarder la carte au format HTML
m.save(args.html_output_file)
print("")
print("Fichier '%s' generé." % args.html_output_file)
print("Terminé")
