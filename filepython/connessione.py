# TO DO
# 3. fare le query
# 4. creare delle strade "nuove che intersichino i lotti"
# 5. sistemare la gui
# 6. correggere la parte di creazione dei lotti (per nuovi lotti)

import os
from pymongo import MongoClient, GEOSPHERE
import json
class CatastoManager:
    def __init__(self, username, password, cluster_url, database_name):
        self.client = MongoClient(f'mongodb+srv://{username}:{password}@{cluster_url}/')
        self.database = self.client[database_name]

    def open_close(self):
        print(f"Connessione al database :{database_name}")
        collections = self.database.list_collection_names()
        print(f"Collezioni disponibili nel database: {collections}")

    def get_index_information(self, collection_name):
            collection = self.database[collection_name]
            index_info = collection.index_information()

            # Stampa le informazioni sugli indici
            for index_name, index_details in index_info.items():
                print(f"Nome dell'indice: {index_name}")
                print(f"Dettagli dell'indice: {index_details}")
                print("\n")

    def insert_data_from_file(self, collection_name, file_path, location_field):
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
        except Exception as e:
            print(f"Errore durante la lettura del file JSON: {str(e)}")
            return

        collection = self.database[collection_name]
        try:
            collection.insert_one(data)
            print(f"Dati dal file '{file_path}' inseriti nella collezione '{collection_name}'.")
        except Exception as e:
            print(f"Errore durante l'inserimento dei dati: {str(e)}")

    def insert_data_from_folder(self, collection_name, folder_path, location_field):
        # Itera attraverso tutti i file nella cartella
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                self.insert_data_from_file(collection_name, file_path, location_field)

    def close_connection(self):
        self.client.close()

    def find_owner(self, collection_name, nome: str, cognome: str = ""):
        # Capitalizza le variabili nome e cognome
        print("Sto cercando...")
        nome_capitalized = nome.capitalize()
        print(nome_capitalized)
        cognome_capitalized = cognome.capitalize()
        print(f"Cerco {nome_capitalized} in collezione {collection_name}")

        # Ottieni la collezione corrente
        collection = self.database[collection_name]

        # Costruisci la query in base ai parametri forniti
        query = {"utenti.proprietario.nome": nome_capitalized}
        if cognome != "":
            query["utenti.proprietario.cognome"] = cognome_capitalized

        # Proiezione dei campi desiderati
        projection = {
        "utenti.proprietario.nome": 1,
        "utenti.proprietario.cognome": 1,
        "utenti.proprietario.cf": 1,
        "utenti.proprietario.data_nascita": 1,
        "utenti.proprietario.luogo_nascita": 1,
        "utenti.proprietario.indirizzo_residenza": 1,
        "utenti.lotti.nome": 1,
        "utenti.lotti.geometry": 1,
        "utenti.lotti.area": 1,
        "utenti.lotti.perimetro": 1,
        "utenti.lotti.centroide.latitudine": 1,
        "utenti.lotti.centroide.longitudine": 1,
        "utenti.lotti.provincia_lotto": 1,
        "_id": 0
    }

        try:
            # Esegui la query
            result = collection.find(query, projection)

            # Stampa o elabora tutti i risultati
            # da migliorare la visualizzazione 
            for documento in result:
                print(documento)
        except Exception as e:
            print(f"Errore durante la ricerca: {str(e)}")

    def find_owner_by_cv(self, collection_name, cf: str):
        cf = cf.lower()
        print(f"Sto cercando codice fiscale: {cf} in collezione {collection_name}")

        collection = self.database[collection_name]

        query = {"utenti.proprietario.cf": cf}

        try:
            result = collection.aggregate([
                {"$match": query},
                {"$project": {
                    "utenti.proprietario.nome": 1,
                    "utenti.proprietario.cognome": 1,
                    "utenti.proprietario.cf": 1,
                    "utenti.proprietario.data_nascita": 1,
                    "utenti.proprietario.luogo_nascita": 1,
                    "utenti.proprietario.indirizzo_residenza": 1,
                    "lotti.nome": "$utenti.lotti.nome",
                    "lotti.geometry": "$utenti.lotti.geometry",
                    "lotti.area": "$utenti.lotti.area",
                    "lotti.perimetro": "$utenti.lotti.perimetro",
                    "lotti.centroide_latitudine": "$utenti.lotti.centroide.latitudine",
                    "lotti.centroide_longitudine": "$utenti.lotti.centroide.longitudine",
                    "lotti.provincia": "$utenti.lotti.provincia_lotto",
                    "_id": 0
                }}
            ])

            for documento in result:
                print(documento)
        except Exception as e:
            print(f"Errore durante la ricerca: {str(e)}")

    def create_geospatial_index(self, collection_name, location_field, index_name=None):
        collection = self.database[collection_name]
        
        if not index_name:
            index_name = f"{location_field}_2dsphere"

        try:
            # Verifica se l'indice esiste già
            existing_indexes = collection.index_information()
            if index_name in existing_indexes:
                print(f"L'indice '{index_name}' esiste già nella collezione '{collection_name}'.")
                return

            # Creazione dell'indice 2dsphere
            collection.create_index([(location_field, "2dsphere")], name=index_name)
            print(f"Indice 2dsphere creato su campo '{location_field}' nella collezione '{collection_name}' con nome '{index_name}'.")
        except Exception as e:
            print(f"Errore durante la creazione dell'indice: {str(e)}")


    def find_owner_by_coordinates(self, collection_name, punto_di_riferimento):
        query = {
            "utenti.lotti.geometry": {
                "$geoIntersects": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [punto_di_riferimento[0], punto_di_riferimento[1]]  # Inverti le coordinate
                    }
                }
            }
        }

        collection = self.database[collection_name]
        print(f"Sto cercando il punto: {punto_di_riferimento[0]},{punto_di_riferimento[1]} in collezione {collection_name}")

        try:
            # Fornisci il nome effettivo dell'indice come hint
            result = collection.find(
                query,
                {
                    "_id": 0,
                    "utenti.proprietario.nome": 1,
                    "utenti.proprietario.cognome": 1,
                    "utenti.proprietario.cf": 1,
                    "utenti.proprietario.data_nascita": 1,
                    "utenti.proprietario.luogo_nascita": 1,
                    "utenti.proprietario.indirizzo_residenza": 1,
                    "utenti.lotti.nome": 1,
                    "utenti.lotti.geometry": 1,
                    "utenti.lotti.area": 1,
                    "utenti.lotti.perimetro": 1,
                    "utenti.lotti.centroide_latitudine": 1,
                    "utenti.lotti.centroide_longitudine": 1,
                    "utenti.lotti.provincia_lotto": 1
                }
            ).hint("geometry.coordinates_2dsphere")   # Specifica il nome dell'indice geospaziale

            # Stampa il piano di esecuzione della query
            print(result.explain())

            for documento in result:
                print(documento)
        except Exception as e:
            print(f"Errore durante la ricerca: {str(e)}")







if __name__ == '__main__':
    username = 'gsavio'
    password = 'Gretina99'
    cluster_url = 'cluster0.fmg5plx.mongodb.net'
    database_name = 'catasto'

    # Creo un'istanza della classe CatastoManager
    manager = CatastoManager(username, password, cluster_url, database_name)
    folder_path = 'json_inserimento'
    location_field = 'geometry.coordinates'

    try:
        print("Operazioni sul database:")
        manager.open_close()
        manager.create_geospatial_index("informazioni_catastali", location_field)
        #manager.insert_data_from_folder("informazioni_catastali", folder_path, location_field)
        manager.get_index_information("informazioni_catastali")
    finally:
        ...
        # Chiudo la connessione alla fine delle operazioni
        #manager.close_connection()
    
    # cerco per nome
    #manager.find_owner_by_cv(collection_name ="informazioni_catastali", cf = "strlnr05c19p220y")

    # Cerco per coordinata
    manager.find_owner_by_coordinates(collection_name="informazioni_catastali", punto_di_riferimento= [45.396990350250306,9.491071330351419])