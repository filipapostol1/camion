import requests

ORS_API_KEY = "INSERISCI_QUI_LA_TUA_CHIAVE_API" 

def ottieni_coordinate(indirizzo):
    try:
        url_nom = "https://nominatim.openstreetmap.org/search"
        q_str = f"{indirizzo}, Italia" if "italia" not in indirizzo.lower() else indirizzo
        res = requests.get(
            url_nom, 
            params={"q": q_str, "format": "json", "limit": 1}, 
            headers={"User-Agent": "ApostolTruckApp/3.0"}, 
            timeout=5
        )
        res.raise_for_status()
        data = res.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except requests.exceptions.RequestException as e:
        print(f"Errore connessione geocoding: {e}")
    except (IndexError, KeyError, ValueError) as e:
        print(f"Errore parsing dati geocoding: {e}")
    return None, None

def calcola_rotta_camion(lat1, lon1, lat2, lon2, api_key=None):
    key = api_key or ORS_API_KEY
    if key and key != "INSERISCI_QUI_LA_TUA_CHIAVE_API":
        try:
            headers = {'Authorization': key, 'Content-Type': 'application/json'}
            body = {"coordinates": [[lon1, lat1], [lon2, lat2]]}
            res = requests.post(
                "https://api.openrouteservice.org/v2/directions/driving-hgv/json", 
                json=body, headers=headers, timeout=8
            )
            if res.status_code == 200:
                return round(res.json()["routes"][0]["summary"]["distance"] / 1000.0, 1)
        except Exception as e:
            print(f"Errore API ORS: {e}")
            
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        return round(res.json()["routes"][0]["distance"] / 1000.0, 1)
    except Exception as e:
        print(f"Errore OSRM: {e}")
    
    return None
