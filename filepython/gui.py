import tkinter as tk
from tkinter import ttk
import folium
from screeninfo import get_monitors
import connessione 

def on_button_click():
    def search_by_coordinates():
        # Get latitude and longitude from entry fields
        latitude = latitude_entry.get()
        longitude = longitude_entry.get()

        # Do something with the coordinates (you can replace this with your logic)
        result_text.set(f"Coordinates Entered: Lat={latitude}, Long={longitude}")

        # ho latitudine e longitudine
       
    # Create a new Toplevel window
    new_page = tk.Toplevel(root)
    new_page.title("Cerca per Coordinate")

    # Add entry fields for latitude and longitude
    latitude_label = ttk.Label(new_page, text="Latitudine:")
    latitude_label.grid(row=0, column=0, padx=5, pady=5)

    latitude_entry = ttk.Entry(new_page)
    latitude_entry.grid(row=0, column=1, padx=5, pady=5)

    longitude_label = ttk.Label(new_page, text="Longitudine:")
    longitude_label.grid(row=1, column=0, padx=5, pady=5)

    longitude_entry = ttk.Entry(new_page)
    longitude_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add a button to trigger the search
    search_button = ttk.Button(new_page, text="Cerca", command=search_by_coordinates)
    search_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Add a label to display the result or any message
    result_text = tk.StringVar()
    result_label = ttk.Label(new_page, textvariable=result_text)
    result_label.grid(row=3, column=0, columnspan=2, pady=10)

# per vedere se  trovi con codice fiscale
def on_search_button_click():
    new_page = tk.Toplevel(root)
    new_page.title("Nuova Pagina")
    label = ttk.Label(new_page, text="Hai premuto Cerca Codice Fiscale")
    label.pack(padx=150, pady=150)

# per vedere se ci sono lotti coinvolti in nuove costruzioni
def on_search_newstreet_button_click():
    new_page = tk.Toplevel(root)
    new_page.title("Nuova Pagina")
    label = ttk.Label(new_page, text="Hai premuto Cerca Strada")
    label.pack(padx=150, pady=150)

def on_exit_button_click():
    root.destroy()



# Create the main window
root = tk.Tk()
root.title("CATASTO")

# Center the main window
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set style for buttons
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 16))

# Add a centered title
title_label = ttk.Label(root, text="CATASTO", font=("Helvetica", 20))
title_label.pack(pady=20)

# Add buttons for different actions
map_button = ttk.Button(root, text="Cerca Punto", command=on_button_click)
map_button.pack(pady=10)

search_button = ttk.Button(root, text="Cerca Nome", command=on_search_button_click)
search_button.pack(pady=10)

search_newstreet = ttk.Button(root, text="Cerca Strada", command=on_search_newstreet_button_click)
search_newstreet.pack(pady=10)

# Add an exit button
exit_button = ttk.Button(root, text="Esci", command=on_exit_button_click)
exit_button.pack(side=tk.BOTTOM, anchor=tk.SW, pady=6)

# Start the Tkinter event loop
root.mainloop()