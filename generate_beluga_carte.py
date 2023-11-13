import folium
import pandas as pd
from waze_route_calculator import WazeRouteCalculator
import requests
from folium.plugins import Search
import argparse

COLORS = {
    "blue": "blue",
    "green": "green",
    "red": "red",
    "yellow": "orange",
}
params = {
    "location": "sans numéro de rue",  # sans numéro de rue ou 'bureau de poste le plus proche"
}


def get_official_adress_from_coordinates(lat, long):
    # check l'adresse officielle sur le site du gouvernement
    URL_GOUV = (
        "https://api-adresse.data.gouv.fr/reverse/?lon=%f&lat=%f&type=street&limit=1"
        % (long, lat)
    )
    response = requests.get(URL_GOUV)
    # retourne un truc comme ca
    # {"type":"FeatureCollection","version":"draft","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[3.876086,43.611302]},"properties":{"label":"Place Chabaneau 34000 Montpellier","score":0.9999999481017439,"id":"34172_1170","name":"Place Chabaneau","postcode":"34000","citycode":"34172","x":770745.31,"y":6279531.37,"city":"Montpellier","context":"34, Hérault, Occitanie","type":"street","importance":0.67279,"street":"Place Chabaneau","distance":11}}],"attribution":"BAN","licence":"ETALAB-2.0","filters":{"type":"street"},"center":[3.8761,43.6112],"limit":1}

    if response.status_code == 200:
        data = response.json()
        return data["features"][0]["properties"]["label"]
    return None


def get_coordinates(address):
    """get les coordonnées lat/long en fonction de l'adresse par waze (l'api de laposte fonctionne moins
    bien. elle est beaucoup moins tolérante sur l'exactitude de l'adresse)"""
    waze = WazeRouteCalculator()
    location_dict = waze.address_to_coords(address)
    lat = location_dict["lat"]
    long = location_dict["lon"]
    print("- traite  l'adresse '%s'" % address)
    if location_dict:
        if params["location"] == "sans numéro de rue":
            return [lat, long]
        elif params["location"] == "bureau de poste le plus proche":
            official_adresse = get_official_adress_from_coordinates(lat, long)
            # le api de la poste ne fonctionne pas bien
            # lat,long = get_nearest_post_office(official_adresse)
            return [lat, long]
        else:
            return [lat, long]
    else:
        return [43.6109, 3.8772]


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
title_html = (
    '<h3 align="center" style="font-size:20px"><b>Beluga ! </b> adresse %s</h3>'
    % params["location"]
)
m.get_root().html.add_child(folium.Element(title_html))

# creation des layers
lutin_group = folium.FeatureGroup(name="Lutin")
louveteau_group = folium.FeatureGroup(name="Louveteau")
eclai_group = folium.FeatureGroup(name="Eclai.es")
aines_group = folium.FeatureGroup(name="Aines")
respons_group = folium.FeatureGroup(name="Respons")

m.add_child(lutin_group)
m.add_child(louveteau_group)
m.add_child(eclai_group)
m.add_child(aines_group)
m.add_child(respons_group)

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
        location=get_coordinates(
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
    elif df["groupe"][index] == "Respons":
        marker.add_to(respons_group)

# ajout du layer control
folium.LayerControl().add_to(m)

# Sauvegarder la carte au format HTML
m.save(args.html_output_file)
print("")
print("Fichier '%s' generé." % args.html_output_file)
print("Terminé")
