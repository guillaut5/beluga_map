# -*- coding: utf-8 -*-
"""Waze route calculator"""

import logging
import requests
import random


class WRCError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class AdressUtils(object):
    """Calculate actual route time and distance with Waze API and Gouv.fr API"""

    WAZE_URL = "https://www.waze.com/"

    def __init__(self, region="EU", log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)

        region = region.upper()
        self.region = region

    def get_official_adress_from_coordinates(self, lat, long):
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

    def get_coordinates(self, address):
        """get les coordonnées lat/long en fonction de l'adresse par waze (l'api de laposte fonctionne moins
        bien. elle est beaucoup moins tolérante sur l'exactitude de l'adresse)

        ajout un composante random qui ajouter un approximation de 50m
        pour eviter que 2 marker ne se juxstapose"""
        location_dict = self.address_to_coords(address)
        #
        # La terre fait 40km de circonference en 360°
        # Je veux rajouter un random de 50m en surface
        # donc je faist 50m/40 000 0000m * 360° pour avoir approximativement l'angle
        # correspondant a 50m en surface
        #
        lat = location_dict["lat"] + random.uniform(-0.00090, 0.0009)
        long = location_dict["lon"] + random.uniform(-0.0009, 0.0009)
        print("- traite  l'adresse '%s'" % address)
        if location_dict:
            return [lat, long]
        else:
            return [43.6109, 3.8772]

    def address_to_coords(self, address):
        """Convert address to coordinates"""

        response_json = self.get_location_from_adress(address)
        lon = response_json["location"]["lon"]
        lat = response_json["location"]["lat"]
        bounds = response_json["bounds"]  # sometimes the coords don't match up
        if bounds is not None:
            bounds["top"], bounds["bottom"] = max(bounds["top"], bounds["bottom"]), min(
                bounds["top"], bounds["bottom"]
            )
            bounds["left"], bounds["right"] = min(bounds["left"], bounds["right"]), max(
                bounds["left"], bounds["right"]
            )
        else:
            bounds = {}
        return {"lon": lon, "lat": lat, "bounds": bounds}

    def get_location_from_adress(self, address):
        EU_BASE_COORDS = {"lon": 19.040, "lat": 47.498}
        US_BASE_COORDS = {"lon": -74.006, "lat": 40.713}
        IL_BASE_COORDS = {"lon": 35.214, "lat": 31.768}
        BASE_COORDS = dict(US=US_BASE_COORDS, EU=EU_BASE_COORDS, IL=IL_BASE_COORDS)[
            self.region
        ]
        # the origin of the request can make a difference in the result

        get_cords = "SearchServer/mozi?"
        url_options = {
            "q": address,
            "lang": "eng",
            "origin": "livemap",
            "lon": BASE_COORDS["lon"],
            "lat": BASE_COORDS["lat"],
        }
        response = requests.get(self.WAZE_URL + get_cords, params=url_options)
        response_json = response.json()[0]
        response_json["lon"] = response_json["location"]["lon"]
        response_json["lat"] = response_json["location"]["lat"]
        return response_json
