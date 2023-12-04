from pykml import parser
import pandas as pd
import funzioni_coordinate
import re
import chardet
import json
import os
import random

def salva_json_in_cartella(nome_file, dati_json, cartella):
    percorso_completo = os.path.join(cartella, nome_file)
    with open(percorso_completo, 'w') as file_json:
        json.dump(dati_json, file_json, indent=2)
    print(f"Il file {nome_file} è stato salvato nella cartella {cartella}")

def extract_data(placemark, data_dict):
    name = placemark.find(".//kml:name", namespaces=namespace)
    longitude = placemark.find(".//kml:LookAt/kml:longitude", namespaces=namespace)
    latitude = placemark.find(".//kml:LookAt/kml:latitude", namespaces=namespace)
    
    if name is not None and longitude is not None and latitude is not None:
        name_text = name.text
        if name_text not in data_dict:
            data_dict[name_text] = {'index': len(data_dict) + 1, 'data': []}
        data_entry = {'longitude': float(longitude.text), 'latitude': float(latitude.text)}
        data_dict[name_text]['data'].append(data_entry)

def parse(root, data_dict):
    for elt in root.getchildren():
        tag = elt.tag.split('}')[-1]  # Extract tag name without using re
        if tag in ["Document", "Folder"]:
            parse(elt, data_dict)
        elif tag == "Placemark":
            extract_data(elt, data_dict)

def transform_name(name):
    if re.search(r'\d', name) and re.search(r'[a-zA-Z]', name):  # Check if both letter and number are present
        # Remove numeric part and append 'T'
        return re.sub(r'\d', '', name) + 'T'
    return name

def crea_json(df_persone, df_coordinate):    
    quantitativo_lotti = random.randint(1, 3)


if __name__ == '__main__':
    file_path = r"./dati/coordinate_2.kml"
    with open(file_path, 'r') as f:
        root = parser.parse(f).getroot()

    namespace = {"kml": 'http://www.opengis.net/kml/2.2'}
    
    data_dict = {} 
    parse(root, data_dict)

    df = pd.DataFrame([(name, entry['longitude'], entry['latitude']) 
                       for name, data in data_dict.items() 
                       for entry in data['data']], 
                      columns=['Name', 'Longitude', 'Latitude'])

    df['Name'] = df['Name'].apply(transform_name)
    print(df)


    percorso_csv = r"./dati/dataset.csv"
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Rileva l'encoding del file CSV
    with open(percorso_csv, 'rb') as f:
        result = chardet.detect(f.read())

    # Leggi il file CSV come un DataFrame utilizzando l'encoding rilevato
    dataframe = pd.read_csv(percorso_csv, header=0, encoding=result['encoding'], sep=';')
    print(dataframe)

    print(df)

    # Raggruppare per nome e creare una lista di tuple (latitudine, longitudine)
    grouped_data = df.groupby('Name').apply(lambda group: list(zip(group['Latitude'], group['Longitude']))).reset_index(name='Coordinates')
    subset = grouped_data['Coordinates']

    print(subset)
    print(dataframe)
    


    

    # Unisci i dati raggruppati nel DataFrame originale
    #dataframe = pd.merge(dataframe, grouped_data, on='Name', how='left')







