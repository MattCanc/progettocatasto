from pykml import parser
import re
import pandas as pd

def extract_data(placemark, data_dict):
    name = placemark.find(".//kml:name", namespaces=namespace)
    longitude = placemark.find(".//kml:LookAt/kml:longitude", namespaces=namespace)
    latitude = placemark.find(".//kml:LookAt/kml:latitude", namespaces=namespace)
    
    if name is not None:
        name_text = name.text
        if name_text not in data_dict:
            data_dict[name_text] = {'index': len(data_dict) + 1, 'data': []}
        data_entry = {'longitude': float(longitude.text), 'latitude': float(latitude.text)}
        data_dict[name_text]['data'].append(data_entry)

def parse(root, data_dict):
    for elt in root.getchildren():
        tag = re.sub(r'^.*\}', '', elt.tag)
        if tag in ["Document", "Folder"]:
            parse(elt, data_dict)
        elif tag == "Placemark":
            extract_data(elt, data_dict)

if __name__ == '__main__':
    file_path = r"./coordinate_2.kml"
    with open(file_path, 'r') as f:
        root = parser.parse(f).getroot()

    namespace = {"kml": 'http://www.opengis.net/kml/2.2'}
    
    data_dict = {}  # Dizionario per memorizzare i dati
    parse(root, data_dict)

    # Stampare il risultato
    for name, data in data_dict.items():
        print(f"Nome {name} (Index {data['index']}):")
        for entry in data['data']:
            print(f"  Longitude: {entry['longitude']}, Latitude: {entry['latitude']}")
