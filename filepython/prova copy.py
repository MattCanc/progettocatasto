from tkinter import *
import folium
import geocoder

basemaps = ["OpenStreetMap", "MapQuest Open", "MapQuest Open Aerial",
            "Mapbox Bright", "Mapbox Control Room", "CartoDB dark_matter",
            "CartoDB positron", "Stamen Terrain", "Stamen Toner",
            "Stamen Watercolor"]

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def make_map(city, state, basemap):
    user_place = f"{city}, {state}"
    g = geocoder.google(user_place)

    if not g.ok:
        print(f"Error: Unable to geocode the provided location ({user_place}).")
        return

    latlng = g.latlng

    if latlng is None:
        print("Error: Geocoder did not return latitude and longitude.")
        return

    x, y = latlng

    xxx = geocoder.google([x, y], method='reverse')
    city_name = xxx.city

    mappy = folium.Map(location=[x, y], tiles=basemap, zoom_start=13)
    folium.Marker([x, y], popup=city_name).add_to(mappy)

    mappy.save('YourMap.html')
    print("Map generated successfully!")

def ok():
    print("Basemap:", var1.get())
    print("City:", userCity.get())
    print("State:", var2.get())
    base = var1.get()
    city = userCity.get()
    state = var2.get()
    make_map(city, state, base)

master = Tk()
master.title("Make me a Map!")

Label(master, text="Pick a map").grid(row=0)
Label(master, text="City").grid(row=1)
Label(master, text="State").grid(row=2)

userCity = Entry(master)
userCity.grid(row=1, column=1)

var1 = StringVar(master)
var1.set(basemaps[8])  # initial value
option1 = OptionMenu(master, var1, *basemaps)
option1.grid(row=0, column=1)

var2 = StringVar(master)
var2.set(states[0])  # initial value
option2 = OptionMenu(master, var2, *states)
option2.grid(row=2, column=1)

button = Button(master, text="OK", command=ok)
button.grid(row=5, column=0)

mainloop()
