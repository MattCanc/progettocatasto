from pykml import parser
import pandas as pd
import re

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
    
    data_dict = {}  # Dictionary to store data
    parse(root, data_dict)

    # Convert data_dict to a DataFrame
    df = pd.DataFrame([(name, entry['longitude'], entry['latitude']) 
                       for name, data in data_dict.items() 
                       for entry in data['data']], 
                      columns=['Name', 'Longitude', 'Latitude'])

    # Print the DataFrame
    print(df)

    # Apply the transformation to the 'Name' column
    df['Name'] = df['Name'].apply(transform_name)

    # Print the updated DataFrame
    print(df)

