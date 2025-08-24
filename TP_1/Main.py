from datetime import datetime as dt
data = {}
file = open("C:\\Users\\cjoaq\\OneDrive\\Documentos\\GitHub\\DesarrolloDeHerramientasDeSoftware\\TP_1\\Data\\registro_temperatura365d_smn.txt", "r")

# Read dataset and load it into a dictionary grouped by station name
for line in file:
    parts = line.strip().split(maxsplit = 3)
    
    if len(parts) < 4 or parts[0] == "Fecha" or parts[0].startswith("-"):
        continue
    
    date, tmaxm, tmin, name = parts
    
    try:
        date = dt.strptime(date, "%d%m%Y").date()
        tmaxm = float(tmaxm)
        tmin = float(tmin)
    except ValueError:
        tmaxm = None
        tmin = None

    if name not in data:
        data[name] = {"DATE": [], "TMAX": [], "TMIN": []}
    data[name]["DATE"].append(date)
    data[name]["TMAX"].append(tmaxm)
    data[name]["TMIN"].append(tmin)

# Write searches to file
with open("First_Report.txt", "w") as f:
    # =============================
    # Report: max TMAX and min TMIN for each station in the last year
    # =============================
    date_begin = "01012025"
    date_end = "31122025"
    date_begin = dt.strptime(date_begin, "%d%m%Y").date()
    date_end = dt.strptime(date_end, "%d%m%Y").date()
    
    f.write(f"=== Max TMAX and Min TMIN registered between {date_begin} and {date_end} for each station ===\n")
    f.write(f"{'STATION NAME':<40} {'DATE':<10} {'TMAX':>7} {'TMIN':>7}\n")
    f.write(f"{'-'*40} {'-'*10} {'-'*7} {'-'*7}\n")

    for station in sorted(data.keys()):
        values = data[station]
        max_tmax = None
        min_tmin = None
        
        for i, date in enumerate(values["DATE"]):
            if date_begin <= date <= date_end:
                tmax = values["TMAX"][i]
                tmin = values["TMIN"][i]
                
                if tmax is not None:
                    if max_tmax is None or tmax > max_tmax:
                        max_tmax = tmax
                        max_tmax_date = date
                        
                if tmin is not None:
                    if min_tmin is None or tmin < min_tmin:
                        min_tmin = tmin
                        min_tmin_date = date
        # Formatting                
        if max_tmax is not None:
            max_tmax_str = f"{max_tmax:.1f}"
            max_tmax_date_str = max_tmax_date.strftime("%d/%m/%Y")
        else: 
            max_tmax_str = f"{'N/A':>7}"
            max_tmax_date_str = f"{'N/A':>10}"
            
        if min_tmin is not None:
            min_tmin_str = f"{min_tmin:.1f}"
            min_tmin_date_str = min_tmin_date.strftime("%d/%m/%Y")
        else:
            min_tmin_str = f"{'N/A':>7}"
            min_tmin_date_str = f"{'N/A':>10}"

        f.write(f"{station:<40} {max_tmax_date_str:<10} {max_tmax_str:>7} {min_tmin_str:>7}\n")

file.close()