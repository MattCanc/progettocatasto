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

finally:
    ...