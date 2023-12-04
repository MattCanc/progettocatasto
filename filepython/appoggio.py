from bson import ObjectId
from pymongo import MongoClient

def openClose():
    client = MongoClient('mongodb+srv://gsavio:Gretina99@cluster0.fmg5plx.mongodb.net/catasto')

    db = client["does-not-exist"]
    print(db)

    db = client.sample_mflix
    print(db)

    db = client["informazioni_catastali"]
    print(db)

def insert():
    client = MongoClient('mongodb+srv://gsavio:Gretina99@cluster0.fmg5plx.mongodb.net/sample_mflix')

    db = client["sample_mflix"]
    print(db)

    coll = db["tickets"]
    print(coll)

    ticket = {
        "code": "qweQWE123",
        "possible_dates" : ["220425", "220523"]
    }
    x = coll.insert_one(ticket)
    print(f"objectid ${x.inserted_id}")

    print(x.acknowledged)

    document = coll.find_one({'_id': x.inserted_id})
    print(document)
    document = coll.find_one({'_id': ObjectId("626a4a45799739942a888695")})

    print(document)

    client.close()

def find():
    client = MongoClient('mongodb+srv://gsavio:Gretina99@cluster0.fmg5plx.mongodb.net/sample_mflix')

    query = {
        "year": 2000
    }
    projection = {
        "year": 1,
        "title": 1,
        "_id": 0
    }
    for post in client.sample_mflix.movies.find(
            filter=query,
            projection=projection,
            limit=4):
        print(post)

    query = {
        "year": {"$eq": 2010}
    }
    projection = {
        "year": 1,
        "title": 1,
        "_id": 0
    }
    for post in client.sample_mflix.movies.find(filter=query, projection=projection, limit=4):
        print(post)

    # Film italiano oiù recente
    query = {
        "countries": "Italy"
    }
    projection = {
        "year": 1,
        "title": 1,
        "countries":1,
        "_id": 0
        }
    
    sort ={"year": -1}
    
    for post in client.sample_mflix.movies.find(filter=query, projection=projection, sort=sort,limit=1):
        print("film italiano più recente")
        print(post)

    #film italiano più corto
    query = {
    "countries": {"$in": ["Italy"]},
    "runtime": {"$exists": True}
    }
    
    projection = {"year": 1,
        "title": 1,
        "countries":1,
        "runtime" : 1,
        "_id": 0}
    
    sort ={"runtime":1}

    print("film italiano più corto")
    for post in client.sample_mflix.movies.find(filter=query, projection=projection, sort=sort,limit=2):
        
        print(post)

    client.close()

if __name__ == '__main__':
    openClose()
