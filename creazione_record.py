# Qua abbiamo intenzione di creare i campi da inserire nel db
# stiamo creando dei lotti utilizzando google heart
# dobbiamo fare in modo che riusciamo ad inserire tutto

import simplekml

def leggi_file_kml(nome_file):
    kml = simplekml.Kml()
    kml_file = open(nome_file, 'r').read()
    kml.from_string(kml_file)
    
    for placemark in kml.features():
        # Qui puoi accedere ai dati del placemark e fare quello che serve
        print("Nome:", placemark.name)
        print("Coordinate:", placemark.geometry.coords)

if __name__ == "__main__":
    nome_file_kml = "tuo_file.kml"
    leggi_file_kml(nome_file_kml)
