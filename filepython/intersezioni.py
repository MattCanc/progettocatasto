from pymongo import MongoClient

# Connessione al database
username = 'gsavio'
password = 'Gretina99'
cluster_url = 'cluster0.fmg5plx.mongodb.net'

client = MongoClient("mongodb+srv://{}:{}@{}/".format(username, password, cluster_url))
db = client["catasto"]
collection = db["informazioni_catastali"]
collection.create_index([("utenti.lotti.geometry", "2dsphere")])


# Costruisci la struttura della query
query = {
    "utenti.lotti.geometry": {
        "$geoIntersects": {
            "$geometry": {
                "type": "LineString",
                "coordinates": [
                    [13.417530680516165, 46.132712096467856],
                    [13.689399686236868, 46.15415842000283]
                ]  
            }
        }
    }
}

try:
    # Remove the incorrect hint
    result = collection.find(
        query,
        {
            "_id": 0,
            "utenti.proprietario.nome": 1,
            "utenti.proprietario.cognome": 1,
            "utenti.proprietario.cf": 1,
            # Add other fields you want to retrieve
        }
    ) 

    # Print the execution plan of the query
    print(collection.find(query).explain())

    for documento in result:
        print(documento)

except Exception as e:
    print(f"Errore durante la ricerca: {str(e)}")


