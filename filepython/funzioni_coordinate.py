import os
import json
from shapely.geometry import Polygon
from pyproj import Transformer
from geopy.geocoders import Nominatim

import json
from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj

def converti_in_metri_quadrati(geometry):
    # Converte le coordinate geografiche in metri quadrati
    project = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform
    geometry_in_metri = transform(project, geometry)
    return geometry_in_metri

def trova_provincia(latitudine, longitudine):
    geolocator = Nominatim(user_agent="trova_nome_citta")
    location = geolocator.reverse((latitudine, longitudine), language="it")

    if location is not None:
        address = location.raw.get("address", {})
        provincia = address.get("state_district") or address.get("state") or address.get("county")
        return provincia or "Non Trovato"
    else:
        return "Non Trovato"


def calcola_campi_vuoti_centroide_area_perimetro(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for utente in data['utenti']:
        for lotto in utente['lotti']:
            # Calcola l'area e il perimetro utilizzando la libreria Shapely
            coordinates = lotto['geometry']['coordinates'][0]
            polygon = Polygon(coordinates)

            # Converte le coordinate del poligono in metri quadrati
            polygon_in_metri = converti_in_metri_quadrati(polygon)

            # Calcola l'area e il perimetro
            area_metri_quadrati = round(polygon_in_metri.area, 2)
            perimetro_metri = round(polygon_in_metri.length, 2)

            # Calcola il centroide
            centroide = polygon.centroid
            latitudine, longitudine = centroide.xy

            # Aggiorna i valori nel dizionario del lotto
            lotto['area'] = area_metri_quadrati
            lotto['perimetro'] = perimetro_metri
            lotto['centroide']['latitudine'] = latitudine[0]
            lotto['centroide']['longitudine'] = longitudine[0]

            provincia = trova_provincia(lotto['centroide']['longitudine'], lotto['centroide']['latitudine'])
            

            # Stampa risultati
            print(f"Lotto {lotto['nome']}:")
            print(f"  Campi vuoti: {campi_vuoti}")
            print(f"  Area: {area_metri_quadrati} m²")
            print(f"  Perimetro: {perimetro_metri} metri")
            print(f"  Centroide: {centroide}\n")
            print(f"  Provincia: {provincia}\n")

    return data

# Esempio di utilizzo
json_path = r'.\json_inserimento\lotto_catasto9.json'
risultato = calcola_campi_vuoti_centroide_area_perimetro(json_path)
