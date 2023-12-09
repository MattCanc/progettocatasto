# Funzioni per le coordinate può diventare una classse
from geopy.geocoders import Nominatim
from shapely.geometry import Polygon

def calcola_area(coordinates):
    polygon = Polygon(coordinates)
    print(polygon.area)
    return polygon.area if polygon.is_valid else 0.0

def calcola_perimetro(coordinates):
    polygon = Polygon(coordinates)
    print(polygon.length)
    return polygon.length if polygon.is_valid else 0.0



def trova_nome_citta(latitudine, longitudine):
    geolocator = Nominatim(user_agent="trova_nome_citta")
    location = geolocator.reverse((latitudine, longitudine), language="it")

    address = location.raw.get("address", {})
    city = address.get("city") or address.get("town") or address.get("village")

    return city or "Non Trovato"


nome = trova_nome_citta(latitudine=10.58785631141577, longitudine=43.09965718530952)
print(nome)
