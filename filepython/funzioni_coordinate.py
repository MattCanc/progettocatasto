import os
import json
from geopy.geocoders import Nominatim
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
            lotto['provincia_lotto'] = provincia

            # Stampa risultati
            print(f"Lotto {lotto['nome']}:")
            print(f"  Area: {area_metri_quadrati} m²")
            print(f"  Perimetro: {perimetro_metri} metri")
            print(f"  Centroide: {centroide}\n")
            print(f"  Provincia: {provincia}\n")

    # Sovrascrivi il file JSON con i risultati
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

    return data

cartella_json = r'.\json_inserimento'

# Itera sui file nella cartella
#for filename in os.listdir(cartella_json):
    #if filename.endswith(".json"):
        #json_path = os.path.join(cartella_json, filename)
        #print(json_path)
        #risultato = calcola_campi_vuoti_centroide_area_perimetro(json_path)

risultato = calcola_campi_vuoti_centroide_area_perimetro(f"./json_strade/lotto_catasto_strada2.json")