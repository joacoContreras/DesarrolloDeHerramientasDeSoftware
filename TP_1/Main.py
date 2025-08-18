data = {}
file = open("C:\\Users\\cjoaq\\OneDrive\\Documentos\\GitHub\\DesarrolloDeHerramientasDeSoftware\\TP_1\\Data\\registro_temperatura365d_smn.txt", "r")

for line in file:
    parts = line.strip().split(maxsplit = 3)
    
    if len(parts) < 4 or parts[0] == "Fecha" or parts[0].startswith("-"):
        continue
    
    fecha, tmaxm, tmin, nombre = parts
    row = {
        "FECHA": fecha,
        "TMAX": tmaxm,
        "TMIN": tmin,
        "NOMBRE": nombre.strip()
    }
    data.setdefault(nombre, []).append(row)
    
for r in data["BASE CARLINI (EX JUBANY)"]:
    print(r)


file.close()