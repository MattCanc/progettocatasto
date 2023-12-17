import os
from pymongo import MongoClient, GEOSPHERE
import json
from shapely.geometry import Polygon, LineString
from shapely.geometry import LineString, mapping
from connessione import CatastoManager
import tkinter as tk
from tkinter import ttk
import folium
from screeninfo import get_monitors
import connessione 


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
    manager.create_2d_index("strade_in_costruzione", location_field)
    manager.get_index_information("informazioni_catastali")
    manager.get_index_information("strade_in_costruzione")
    print("Scegli un'opzione:")
    print("1. Cerca lotti da codice fiscale (CV)")
    print("2. Cerca lotti da coordinate")
    print("3. Cerca nuove strade")
    scelta = input("Inserisci il numero dell'opzione desiderata: ")
    if scelta == "1":
        cf = input("Inserisci il codice fiscale (CV): ")
        lotti = manager.find_owner_by_cv(collection_name="informazioni_catastali", cf=cf)
        manager.stampa(lotti)

    elif scelta == "2":
        latitudine = float(input("Inserisci la latitudine: "))
        longitudine = float(input("Inserisci la longitudine: "))
        lotti = manager.find_owner_by_coordinates(collection_name="informazioni_catastali",punto_di_riferimento=[longitudine, latitudine])
        manager.stampa_dati(lotti)
    elif scelta == "3":
        manager.find_new_streets()
    else:
        print('non valido')
finally:
    ...