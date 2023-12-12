# TO DO
# 1. trasformare in clase queste funzioni
# 2. popolare il db
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
        collections = self.database.list_collection_names()
        print(f"Collezioni disponibili nel database: {collections}")

    def create_geospatial_index(self, collection_name, location_field):
        collection = self.database[collection_name]
        # Creazione dell'indice 2dsphere
        collection.create_index([(location_field, GEOSPHERE)])
        print(f"Indice 2dsphere creato su campo '{location_field}' nella collezione '{collection_name}'.")

    def insert_data_from_file(self, collection_name, file_path, location_field):
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
        except Exception as e:
            print(f"Errore durante la lettura del file JSON: {str(e)}")
            return

        collection = self.database[collection_name]
        collection.insert_one(data)

        print(f"Dati dal file '{file_path}' inseriti nella collezione '{collection_name}'.")

    def insert_data_from_folder(self, collection_name, folder_path, location_field):
        # Itera attraverso tutti i file nella cartella
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                self.insert_data_from_file(collection_name, file_path, location_field)

    def close_connection(self):
        self.client.close()

if __name__ == '__main__':
    username = 'gsavio'
    password = 'Gretina99'
    cluster_url = 'cluster0.fmg5plx.mongodb.net'
    database_name = 'catasto'

    # Creo un'istanza della classe CatastoManager
    manager = CatastoManager(username, password, cluster_url, database_name)
    folder_path = 'json_inserimento'
    
    try:
        print("Operazioni sul database:")
        manager.open_close()
        location_field = 'geometry.coordinates'  
        manager.insert_data_from_folder("informazioni_catastali", folder_path, location_field)
        manager.create_geospatial_index("informazioni_catastali", location_field)
        
        

    finally:
        # Chiudo la connessione alla fine delle operazioni
        manager.close_connection()
