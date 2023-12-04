# Funzioni per le coordinate può diventare una classse

def calcola_punto_centrale(coordinates):
    num_punti = len(coordinates)
    media_latitudine = sum(lat for lat, _ in coordinates) / num_punti
    media_longitudine = sum(lon for _, lon in coordinates) / num_punti
    return (media_latitudine, media_longitudine)

def calcola_area(coordinates):
    area = 0.0
    for i in range(len(coordinates) - 1):
        xi, yi = coordinates[i]
        xi1, yi1 = coordinates[i + 1]
        area += (xi * yi1 - xi1 * yi)
    area = abs(area) / 2.0
    return area

def calcola_perimetro(coordinates):
    perimetro = 0.0
    for i in range(len(coordinates) - 1):
        xi, yi = coordinates[i]
        xi1, yi1 = coordinates[i + 1]
        perimetro += ((xi1 - xi)**2 + (yi1 - yi)**2)**0.5
    return perimetro


