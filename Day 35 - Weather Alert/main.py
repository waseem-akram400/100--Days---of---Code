import requests

# Aapki API Key
API_KEY = "e7b55f4141812f99910e12fa9c8ffcd3"

# Multan ki Location
MY_LAT = 30.1575
MY_LON = 71.5249

print(f"Checking the weather for Multan, PK...")

# OpenWeatherMap ka API link
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": API_KEY,
    "cnt": 4 # Agle 12 ghanton ka mausam
}

try:
    response = requests.get(OWM_Endpoint, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()

    will_rain = False

    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 700:
            will_rain = True

    if will_rain:
        print("Barish hone wali hai! Chhatri le jao ☔")
    else:
        print("Mausam saaf hai, barish nahi hogi.")

except Exception as e:
    print(f"Something went wrong: {e}")