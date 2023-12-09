from pykml import parser
import pandas as pd
import funzioni_coordinate as fc
from shapely.geometry import Polygon
import re
import chardet
import json
import os
import random

def salva_json_in_cartella(nome_file, dati_json, cartella):
    percorso_completo = os.path.join(cartella, nome_file)
    try:
        with open(percorso_completo, 'w') as file_json:
            json.dump(dati_json, file_json, indent=2)
        print(f"Il file {nome_file} è stato salvato nella cartella {cartella}")
    except:
        print(f"Errore nel salvataggio del file Json {nome_file} nella cartella: {cartella}")

    
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

def crea_struttura_json(df_persone: pd.DataFrame, df_coordinate: pd.DataFrame):
    if not df_persone.empty:
        record_persone = df_persone.iloc[0]

        json_data = {
            "utenti": [
                {
                    "proprietario": {
                        "nome": record_persone["proprietario_nome"],
                        "cognome": record_persone["proprietario_cognome"],
                        "cf": record_persone["proprietario_cf"],
                        "data_nascita": record_persone["data_nasc"],
                        "luogo_nascita": record_persone["luogo_nasc"],
                        "indirizzo_residenza": record_persone["indirizzo_residenza"]
                    },
                    "lotti": []
                }
            ]
        }

        lista_lotti = []

        for i, coordinates_list in enumerate(df_coordinate['Coordinates']):
            # Make sure to convert to a list if needed
            coordinates = list(coordinates_list)
            print(coordinates)

            # Creazione del poligono utilizzando shapely
            polygon = Polygon(coordinates)

            area = fc.calcola_area(coordinates)
            perimetro = fc.calcola_perimetro(coordinates)

            lotto = {
                "nome": f"lotto di proprietà {i}",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [list(polygon.exterior.coords)]
                },
                "area": area,
                "perimetro": perimetro,
                "centroide": {"latitudine": polygon.centroid.y, "longitudine": polygon.centroid.x},
                "provincia_lotto": fc.trova_nome_citta(longitudine=polygon.centroid.y, latitudine=polygon.centroid.x)
            }

            # Aggiungi il lotto alla lista dei lotti
            lista_lotti.append(lotto)

        # Aggiungi la lista di lotti all'utente
        json_data["utenti"][0]["lotti"] = lista_lotti

        return json_data
    else:
        print("DataFrame df_persone is empty.")
        return None
    
    
# Utilizza la funzione crea_struttura_json per riempire i documenti
def crea_json(df_persone, df_coordinate, path_cartella):
    contatore_nomi = 0
    while not df_coordinate.empty and not df_persone.empty:
        quantitativo_lotti = random.randint(1, 3)
        lotti = df_coordinate.head(quantitativo_lotti)
        
        dati_persona = df_persone.tail(1)  # Use tail(1) to get the last row as a DataFrame
        df_persone = df_persone.drop(df_persone.index[-1])

        json_completo = crea_struttura_json(df_persone=dati_persona, df_coordinate=lotti)
        nome_json = f"lotto_catasto{contatore_nomi}"
        salva_json_in_cartella(nome_file=nome_json, dati_json=json_completo, cartella=path_cartella)
        contatore_nomi += 1

    if df_coordinate.empty:
        print("DataFrame df_coordinate is empty.")
    elif df_persone.empty:
        print("DataFrame df_persone is empty.")



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
    # Convert the Series to a DataFrame
    df_coo = pd.DataFrame({subset.name: subset})
    print((df_coo.columns))
    print(type(dataframe))


    # Popolamento della cartella per l'inserimento
    path_json = r"./json_inserimento"
    crea_json(df_persone = dataframe, df_coordinate = df_coo, path_cartella = path_json)
    







