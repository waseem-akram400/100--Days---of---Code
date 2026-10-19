import requests

MY_LAT = 30.1575  # Multan
MY_LONG = 71.5249

def get_iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])
    return iss_lat, iss_long

def iss_is_overhead():
    iss_latitude, iss_longitude = get_iss_location()
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    return False