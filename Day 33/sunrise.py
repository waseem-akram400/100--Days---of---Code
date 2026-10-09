import requests
from datetime import datetime

MY_LAT = 30.1575
MY_LONG = 71.5249

def get_sunrise_sunset():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = datetime.fromisoformat(data["results"]["sunrise"].replace("Z", "+00:00"))
    sunset = datetime.fromisoformat(data["results"]["sunset"].replace("Z", "+00:00"))
    return sunrise, sunset