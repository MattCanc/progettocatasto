from pymongo import MongoClient
from database_connection import get_database_connection, close_database_connection


# Mi connetto, ma devo chiudere la connessione!!
def get_database_connection():
    client = MongoClient('mongodb+srv://gsavio:Gretina99@cluster0.fmg5plx.mongodb.net/')
    return client["catasto"]

# Funzione per chiudere la connessione al database
# se rimane aperta è un bel problema
def close_database_connection(client):
    client.close()

def openClose():
    db = get_database_connection()
    collections = db.list_collection_names()
    print(f"Collezioni disponibili nel database 'catasto': {collections}")
    close_database_connection(db)

def insert():
    db = get_database_connection()
    coll = db["informazioni_catastali"]
    print(coll)

if __name__ == '__main__':
    print("Progetto Catastale")
    openClose()