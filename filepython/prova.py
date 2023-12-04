import tkinter as tk
from tkinter import ttk
from tkinterhtml import HtmlFrame
import folium

def on_button_click():
    # Crea una mappa centrata su una determinata posizione
    m = folium.Map(location=[41.9028, 12.4964], zoom_start=10)

    # Aggiunge un marcatore alla mappa
    folium.Marker(location=[41.9028, 12.4964], popup="Roma").add_to(m)

    # Salva la mappa in un file HTML temporaneo
    m.save("map.html")

    # Crea una finestra per visualizzare la mappa
    map_window = tk.Toplevel(root)
    
    # Carica l'HTML nella finestra utilizzando tkinterhtml
    html_frame = HtmlFrame(map_window)
    html_frame.set_content("<iframe src='map.html' width='100%' height='100%'></iframe>")
    html_frame.pack(fill=tk.BOTH, expand=True)

# Creazione della finestra principale
root = tk.Tk()
root.title("Simulazione Pagina Software con Mappa")

# Aggiunta di un pulsante per visualizzare la mappa
button = ttk.Button(root, text="Visualizza Mappa", command=on_button_click)
button.pack(pady=20)

# Esecuzione della finestra
root.mainloop()
