import tkinter as tk
from tkinter import ttk
import folium
from screeninfo import get_monitors

def on_button_click():
    ...

def on_search_button_click():
    # Implementa la logica per cercare il nome
    # Aggiungi il codice necessario qui
    pass

def on_exit_button_click():
    root.destroy()

# Creazione della finestra principale
root = tk.Tk()
root.title("CATASTO")

# Centra la finestra principale
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Imposta uno stile per i bottoni
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 16))

# Aggiunta del titolo centrato
title_label = ttk.Label(root, text="CATASTO", font=("Helvetica", 20))
title_label.pack(pady=20)

# Aggiunta di un pulsante per visualizzare la mappa
map_button = ttk.Button(root, text="Cerca Punto", command=on_button_click)
map_button.pack(pady=10)

# Aggiunta di un pulsante per cercare il nome
search_button = ttk.Button(root, text="Cerca Nome", command=on_search_button_click)
search_button.pack(pady=10)

# Aggiunta di un pulsante per cercare la strada
search_newstreet = ttk.Button(root, text="Cerca Strada", command=on_search_button_click)
search_newstreet.pack(pady=10)

# Aggiunta di un pulsante per uscire dall'applicazione (posizionato in basso a sinistra)
exit_button = ttk.Button(root, text="Esci", command=on_exit_button_click)
exit_button.pack(side=tk.BOTTOM, anchor=tk.SW, pady=6)

# Esecuzione della finestra
root.mainloop()
