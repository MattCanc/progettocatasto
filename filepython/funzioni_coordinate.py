from geopy.geocoders import Nominatim
from shapely.geometry import Polygon
from pyproj import Transformer

def converti_coordinate(coordinate, input_epsg, output_epsg):
    transformer = Transformer.from_crs(f'epsg:{input_epsg}', f'epsg:{output_epsg}')
    lon, lat = transformer.transform(coordinate[0], coordinate[1])
    return lon, lat

def calcola_area(coordinates, input_epsg=4326, output_epsg=32633):
    converted_coordinates = [converti_coordinate(coord, input_epsg, output_epsg) for coord in coordinates]
    polygon = Polygon(converted_coordinates)
    print(F"AREA : {polygon.area}")
    return polygon.area if polygon.is_valid else 0.0

def calcola_perimetro(coordinates, input_epsg=4326, output_epsg=32633):
    converted_coordinates = [converti_coordinate(coord, input_epsg, output_epsg) for coord in coordinates]
    polygon = Polygon(converted_coordinates)
    print(F"PERIMETRO : {polygon.length}")
    return polygon.length if polygon.is_valid else 0.0

def trova_nome_citta(latitudine, longitudine):
    geolocator = Nominatim(user_agent="trova_nome_citta")
    location = geolocator.reverse((latitudine, longitudine), language="it")
    address = location.raw.get("address", {})
    city = address.get("city") or address.get("town") or address.get("village")

    return city or "Non Trovato"
