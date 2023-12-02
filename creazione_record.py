from pykml import parser
import pandas as pd
import re
import chardet

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

if __name__ == '__main__':
    file_path = r"./coordinate_2.kml"
    with open(file_path, 'r') as f:
        root = parser.parse(f).getroot()

    namespace = {"kml": 'http://www.opengis.net/kml/2.2'}
    
    data_dict = {} 
    parse(root, data_dict)

    # Convert data_dict to a DataFrame
    df = pd.DataFrame([(name, entry['longitude'], entry['latitude']) 
                       for name, data in data_dict.items() 
                       for entry in data['data']], 
                      columns=['Name', 'Longitude', 'Latitude'])

    df['Name'] = df['Name'].apply(transform_name)
    print(df)

    # Percorso del tuo file CSV
    percorso_csv = "./dataset.csv"

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Rileva l'encoding del file CSV
    with open(percorso_csv, 'rb') as f:
        result = chardet.detect(f.read())

    # Leggi il file CSV come un DataFrame utilizzando l'encoding rilevato
    dataframe = pd.read_csv(percorso_csv, header=0, encoding=result['encoding'], sep=';')
    print(dataframe)

    # Aggiungere quattro colonne, che indicano i punti delle coordinate
    dataframe['coordinata_1'] = None
    dataframe['coordinata_2'] = None
    dataframe['coordinata_3'] = None
    dataframe['coordinata_4'] = None

    print(df)

    # Raggruppare per nome e creare una lista di tuple (latitudine, longitudine)
    grouped_data = df.groupby('Name').apply(lambda group: list(zip(group['Latitude'], group['Longitude']))).reset_index(name='Coordinates')
    subset = grouped_data['Coordinates']

    print(subset)
    
    # Iterate through each index and value (row) in the subset Series
    for index, value in subset.items():
        name = value[0]['Name']  # Access the 'Name' attribute from the first tuple in the list
        coordinates_list = value[1]  # Access the list of coordinates from the second element in the tuple

        # Iterate through the coordinates and populate the corresponding columns
    for i in range(min(len(coordinates_list), 4)):
        column_name = f'coordinata_{i + 1}'
        dataframe.loc[dataframe['Name'] == name, column_name] = coordinates_list[i]

    # Print the updated DataFrame
    print(dataframe)


    

    # Unisci i dati raggruppati nel DataFrame originale
    #dataframe = pd.merge(dataframe, grouped_data, on='Name', how='left')







