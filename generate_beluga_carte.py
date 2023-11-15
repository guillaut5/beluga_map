"""
Script Python pour générer une carte interactive des contacts Beluga, facilitant les mises en relation covoiturage.
Le script prend des données de contacts à partir d'un fichier Excel, organise les informations par groupe et génère une carte Folium.
Les marqueurs sur la carte représentent chaque contact avec des icônes colorées en fonction du groupe auquel ils appartiennent.

Utilisation:
1. Assurez-vous d'avoir les bibliothèques requises installées en exécutant :
   pip install folium pandas

2. Exécutez le script depuis la ligne de commande avec les options suivantes :
   python script.py --input fichier_contacts.xlsx --output carte_contacts.html

   Options:
   --input : Spécifie le fichier Excel contenant les données de contacts (par défaut: exemple_contacts.xlsx).
   --output : Spécifie le nom du fichier HTML de sortie contenant la carte (par défaut: carte_contacts.html).

3. La carte générée est sauvegardée dans le fichier HTML spécifié et peut être ouverte dans un navigateur web.
   Elle affiche les contacts organisés par groupes avec des informations détaillées dans les popups des marqueurs.

Note:
- Les adresses sont floutées, et les icônes des marqueurs varient en fonction du groupe et du rôle du parent.
- Les coordonnées doivent être adaptées à chaque lieu de rencontre.
- Les groupes sont organisés en couches pour permettre à l'utilisateur de choisir quels groupes afficher sur la carte.
"""
import folium
import pandas as pd
from adress_utils import AdressUtils
import requests
from folium.plugins import Search
import argparse
import random
import io

# Dictionnaire de couleurs pour les icônes sur la carte
COLORS = {
    "blue": "blue",
    "green": "green",
    "red": "red",
    "yellow": "orange",
}

# Configuration de l'analyseur d'arguments en ligne de commande
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

# Affichage des informations sur les fichiers d'entrée et de sortie
print(
    "generation de la carte a partir du fichier source '%s'\nLa carte sera générée dans le fichier '%s'"
    % (args.xls_input_file, args.html_output_file)
)

# Lecture des données Excel dans un DataFrame Pandas
df = pd.read_excel(args.xls_input_file)
print("")

# Affichage du nombre de contacts lus
print("Lecture de %d contacts" % len(df.index))

# Création d'une carte centrée sur Montpellier avec un zoom initial de 11
m = folium.Map(location=[43.6109, 3.8772], zoom_start=11)

# Ajout d'un titre
title_html = '<h3 align="center" style="font-size:20px"><b>Beluga ! </b> les adresses sont floutées, sans numéro de rue</h3>'
m.get_root().html.add_child(folium.Element(title_html))

# Création de groupes pour organiser les marqueurs
lutin_group = folium.FeatureGroup(name="Lutin.es")
louveteau_group = folium.FeatureGroup(name="Louveteaux.ettes")
eclai_group = folium.FeatureGroup(name="Eclai.es")
aines_group = folium.FeatureGroup(name="Aine.es")

m.add_child(lutin_group)
m.add_child(louveteau_group)
m.add_child(eclai_group)
m.add_child(aines_group)

# Utilisation d'une classe AdressUtils pour obtenir les coordonnées à partir des adresses
adress_utils = AdressUtils()

# Ajout de marqueurs pour chaque contact sur la carte
for index, row in df.iterrows():
    # Construction du contenu de la popup pour chaque marqueur
    popup_content = f"<H3>{row['enfant']}</H3> <h4> 0{row['contact']} </h4> <h5>{row['email']} </h5> <p> {row['parent']}</p>"

    # Définition de l'icône en fonction du groupe et du rôle du parent
    icon = None
    if row["groupe"] == "Lutin.es":
        icon = folium.Icon(color=COLORS["blue"], prefix="fa", icon="hat-wizard")
        if row["parent"] == "Respons":
            icon = folium.Icon(color=COLORS["blue"], prefix="fa", icon="ghost")
    elif row["groupe"] == "Louveteaux.ettes":
        icon = folium.Icon(color=COLORS["yellow"], prefix="fa", icon="paw")
        if row["parent"] == "Respons":
            icon = folium.Icon(color=COLORS["yellow"], prefix="fa", icon="ghost")
    elif row["groupe"] == "Eclai.es":
        icon = folium.Icon(color=COLORS["green"], prefix="fa", icon="face-laugh-squint")
        if row["parent"] == "Respons":
            icon = folium.Icon(color=COLORS["green"], prefix="fa", icon="ghost")
    elif row["groupe"] == "Aine.es":
        icon = folium.Icon(color=COLORS["red"], prefix="fa", icon="rocket")
        if row["parent"] == "Respons":
            icon = folium.Icon(color=COLORS["red"], prefix="fa", icon="ghost")
    else:
        icon = folium.Icon(color=COLORS["red"], icon="info-sign")

    # Création du marqueur avec la popup et l'icône définis
    marker = folium.Marker(
        location=adress_utils.get_coordinates(
            row["adresse floute"]
        ),  # Vous devez remplacer ces coordonnées par celles de chaque lieu de rencontre
        popup=folium.Popup(popup_content, max_width=300),
        name=popup_content,
        icon=icon,
    ).add_to(m)

    # Ajout du marqueur au groupe approprié
    if df["groupe"][index] == "Lutin.es":
        marker.add_to(lutin_group)
    elif df["groupe"][index] == "Louveteaux.ettes":
        marker.add_to(louveteau_group)
    elif df["groupe"][index] == "Eclai.es":
        marker.add_to(eclai_group)
    elif df["groupe"][index] == "Aine.es":
        marker.add_to(aines_group)

# Ajout du contrôle des couches pour permettre à l'utilisateur de choisir quels groupes afficher
folium.LayerControl().add_to(m)

# Sauvegarde de la carte générée au format HTML
m.save(args.html_output_file)

# Affichage de messages de confirmation
print("")
print("Fichier '%s' generé." % args.html_output_file)
print("Terminé")
