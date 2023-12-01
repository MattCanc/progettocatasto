# Qua abbiamo intenzione di creare i campi da inserire nel db
# stiamo creando dei lotti utilizzando google heart
# dobbiamo fare in modo che riusciamo ad inserire tutto

import simplekml
import xml.etree.ElementTree as ET

def leggi_file_kml(nome_file):
    kml = simplekml.Kml()
    
    with open(nome_file, 'r', encoding='utf-8') as kml_file:
        kml_string = kml_file.read()
        root = ET.fromstring(kml_string)
        kml.from_string(ET.tostring(root, encoding='utf8').decode('utf8'))
    
    for placemark in kml.features():
        # Qui puoi accedere ai dati del placemark e fare quello che serve
        print("Nome:", placemark.name)
        print("Coordinate:", placemark.geometry.coords)

if __name__ == "__main__":
    nome_file_kml = r".\coordinate_2.kml"
    leggi_file_kml(nome_file_kml)
