from datetime import datetime as dt

data = {}
path = r"C:\\Users\\cjoaq\\OneDrive\\Documentos\\GitHub\\DesarrolloDeHerramientasDeSoftware\\TP_1\\Data\\registro_temperatura365d_smn.txt"

# Read dataset and load it into a dictionary grouped by station name
with open(path, "r", encoding="utf-8") as file:
    for raw in file:
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        # Saltar cabeceras y guiones
        if parts[0].upper() in ("FECHA", "DATE") or parts[0].startswith("-"):
            continue

        # Fecha
        try:
            date_obj = dt.strptime(parts[0], "%d%m%Y").date()
        except ValueError:
            # línea inválida
            continue

        idx = 1

        # TMAX (opcional)
        tmaxm = None
        if idx < len(parts):
            try:
                tmaxm = float(parts[idx]); idx += 1
            except ValueError:
                tmaxm = None  # si no es número, asumimos que falta

        # TMIN (opcional)
        tmin = None
        if idx < len(parts):
            try:
                tmin = float(parts[idx]); idx += 1
            except ValueError:
                tmin = None  # falta TMIN

        # Nombre de estación: todo lo que queda
        if idx >= len(parts):
            # si no hay nombre, descartamos
            continue
        name = " ".join(parts[idx:]).strip()

        rec = data.setdefault(name, {"DATE": [], "TMAX": [], "TMIN": []})
        rec["DATE"].append(date_obj)
        rec["TMAX"].append(tmaxm)
        rec["TMIN"].append(tmin)

file.close()

with open("Report.txt", "w") as f:
    # =============================
    # Report 1: max TMAX and min TMIN for each station in the last year
    # =============================
    date_begin = dt.strptime("01012025", "%d%m%Y").date()
date_end   = dt.strptime("31122025", "%d%m%Y").date()

with open("Report.txt", "w", encoding="utf-8") as f:
    f.write(f"=== Max TMAX and Min TMIN registered between {date_begin} and {date_end} for each station ===\n")
    f.write(f"{'STATION NAME':<40} {'DATE MAX':<10} {'TMAX':>7} {'DATE MIN':<10} {'TMIN':>7}\n")
    f.write(f"{'-'*40} {'-'*10} {'-'*7} {'-'*10} {'-'*7}\n")

    for station in sorted(data.keys()):
        values = data[station]
        max_tmax, max_tmax_date = None, None
        min_tmin, min_tmin_date = None, None

        for i, d in enumerate(values["DATE"]):
            if not (date_begin <= d <= date_end):
                continue
            tmax = values["TMAX"][i]
            tmin = values["TMIN"][i]

            if tmax is not None and (max_tmax is None or tmax > max_tmax):
                max_tmax = tmax
                max_tmax_date = d

            if tmin is not None and (min_tmin is None or tmin < min_tmin):
                min_tmin = tmin
                min_tmin_date = d

        max_date_str = max_tmax_date.strftime("%d/%m/%Y") if max_tmax_date else "N/A"
        min_date_str = min_tmin_date.strftime("%d/%m/%Y") if min_tmin_date else "N/A"
        tmax_str = f"{max_tmax:7.1f}" if max_tmax is not None else f"{'N/A':>7}"
        tmin_str = f"{min_tmin:7.1f}" if min_tmin is not None else f"{'N/A':>7}"

        f.write(f"{station:<40} {max_date_str:<10} {tmax_str} {min_date_str:<10} {tmin_str}\n")

    # ===================================================  
    # Report 2: Station with the highest temperature range
    # ===================================================

    f.write("\n=== Station with the highest temperature range in the same day ===\n")
    f.write(f"{'STATION NAME':<40} {'DATE':<10} {'RANGE':>7}\n")
    f.write(f"{'-'*40} {'-'*10} {'-'*7}\n")

    max_range = 0
    max_range_station = None
    max_range_date = None
    max_range_tmax = None
    max_range_tmin = None

    for station in sorted(data.keys()):
        values = data[station]
        for i, date in enumerate(values["DATE"]):
            tmax = values["TMAX"][i]
            tmin = values["TMIN"][i]
            if tmax is not None and tmin is not None:
                temp_range = tmax - tmin
                if temp_range > max_range:
                    max_range = temp_range
                    max_range_station = station
                    max_range_date = date
                    max_range_tmax = tmax
                    max_range_tmin = tmin

    if max_range_station is not None:
        f.write(f"{max_range_station:<40} {max_range_date.strftime('%d/%m/%Y'):<10} {max_range:>7.1f}\n")

    # ===================================================
    # Report 3: Station with the lowest temperature range
    # ===================================================

    f.write("\n=== Station with the lowest temperature range in the same day ===\n")
    f.write(f"{'STATION NAME':<40} {'DATE':<10} {'RANGE':>7}\n")
    f.write(f"{'-'*40} {'-'*10} {'-'*7}\n")

    min_range = float('inf')
    min_range_station = None
    min_range_date = None
    min_range_tmax = None
    min_range_tmin = None

    for station in sorted(data.keys()):
        values = data[station]
        for i, date in enumerate(values["DATE"]):
            tmax = values["TMAX"][i]
            tmin = values["TMIN"][i]
            if tmax is not None and tmin is not None:
                temp_range = tmax - tmin
                if temp_range < min_range:
                    min_range = temp_range
                    min_range_station = station
                    min_range_date = date
                    min_range_tmax = tmax
                    min_range_tmin = tmin

    if min_range_station is not None:
        f.write(f"{min_range_station:<40} {min_range_date.strftime('%d/%m/%Y'):<10} {min_range:>7.1f}\n")

    # ===================================================
    # Report 4: Maximum temperature difference between two stations in the same day
    # ===================================================

    f.write("\n=== Maximum temperature difference between two stations in the same day ===\n")
    f.write(f"{'DATE':<10} {'TMAX':>7} {'STATION MAX':<30} {'TMIN':>7} {'STATION MIN':<30} {'DIFF':>7}\n")
    f.write(f"{'-'*10} {'-'*7} {'-'*30} {'-'*7} {'-'*30} {'-'*7}\n")

    all_dates = set()
    for station in data:
        for date in data[station]["DATE"]:
            if date is not None:
                all_dates.add(date)
    all_dates = sorted(all_dates)

    for date in all_dates:
        max_tmax = None
        max_tmax_station = None
        min_tmin = None
        min_tmin_station = None
        for station in data:
            values = data[station]
            for i, d in enumerate(values["DATE"]):
                if d == date:
                    tmax = values["TMAX"][i]
                    tmin = values["TMIN"][i]
                    if tmax is not None:
                        if max_tmax is None or tmax > max_tmax:
                            max_tmax = tmax
                            max_tmax_station = station
                    if tmin is not None:
                        if min_tmin is None or tmin < min_tmin:
                            min_tmin = tmin
                            min_tmin_station = station
        if max_tmax is not None and min_tmin is not None:
            diff = max_tmax - min_tmin
            f.write(f"{date.strftime('%d/%m/%Y'):<10} {max_tmax:>7.1f} {max_tmax_station:<30} {min_tmin:>7.1f} {min_tmin_station:<30} {diff:>7.1f}\n")
        else:
            f.write(f"{date.strftime('%d/%m/%Y'):<10} {'N/A':>7} {'N/A':<30} {'N/A':>7} {'N/A':<30} {'N/A':>7}\n")
            
    # ===================================================
    # Report 5: Minimum temperature difference between two stations in the same day
    # ===================================================

    f.write("\n=== Minimum temperature difference between two stations in the same day ===\n")
    f.write(f"{'DATE':<10} {'TMAX':>7} {'STATION MAX':<30} {'TMIN':>7} {'STATION MIN':<30} {'DIFF':>7}\n")
    f.write(f"{'-'*10} {'-'*7} {'-'*30} {'-'*7} {'-'*30} {'-'*7}\n")

    for date in all_dates:
        min_diff = None
        min_tmax = None
        min_tmax_station = None
        min_tmin = None
        min_tmin_station = None
        stations_for_date = []
        
        for station in data:
            values = data[station]
            for i, d in enumerate(values["DATE"]):
                if d == date:
                    tmax = values["TMAX"][i]
                    tmin = values["TMIN"][i]
                    if tmax is not None and tmin is not None:
                        stations_for_date.append((station, tmax, tmin))
                    
        for s1, tmax1, _ in stations_for_date:
            for s2, _, tmin2 in stations_for_date:
                diff = tmax1 - tmin2
                if min_diff is None or diff < min_diff:
                    min_diff = diff
                    min_tmax = tmax1
                    min_tmax_station = s1
                    min_tmin = tmin2
                    min_tmin_station = s2

        if min_diff is not None:
            f.write(f"{date.strftime('%d/%m/%Y'):<10} {min_tmax:>7.1f} {min_tmax_station:<30} {min_tmin:>7.1f} {min_tmin_station:<30} {min_diff:>7.1f}\n")
        else:
            f.write(f"{date.strftime('%d/%m/%Y'):<10} {'N/A':>7} {'N/A':<30} {'N/A':>7} {'N/A':<30} {'N/A':>7}\n")