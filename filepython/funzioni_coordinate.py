# Funzioni per le coordinate può diventare una classse
from geopy.geocoders import Nominatim

def calcola_punto_centrale(coordinates):
    num_punti = len(coordinates)
    media_latitudine = sum(lat for lat, _ in coordinates) / num_punti
    media_longitudine = sum(lon for _, lon in coordinates) / num_punti
    return (media_latitudine, media_longitudine)

def calcola_area(coordinates):
    area = 0.0
    for i in range(len(coordinates) - 1):
        xi, yi = coordinates[i]
        xi1, yi1 = coordinates[i + 1]
        area += (xi * yi1 - xi1 * yi)
    area = abs(area) / 2.0
    return area

def calcola_perimetro(coordinates):
    perimetro = 0.0
    for i in range(len(coordinates) - 1):
        xi, yi = coordinates[i]
        xi1, yi1 = coordinates[i + 1]
        perimetro += ((xi1 - xi)**2 + (yi1 - yi)**2)**0.5
    return perimetro

def trova_nome_citta(latitudine, longitudine):
    geolocator = Nominatim(user_agent="trova_nome_citta")
    location = geolocator.reverse((latitudine, longitudine), language="it")

    address = location.raw.get("address", {})
    city = address.get("city") or address.get("town") or address.get("village")

    return city or "Nome della città o località non disponibile"



