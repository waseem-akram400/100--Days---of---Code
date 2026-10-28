from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(city):
    # Pehle shehar ke latitude aur longitude hasil karein
    geo_response = requests.get(
        GEO_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=15
    )
    geo_response.raise_for_status()
    places = geo_response.json().get("results", [])

    if not places:
        return None, f"'{city}' ka shehar nahi mila. Naam dobara check karein."

    place = places[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Ab coordinates ki madad se mausam hasil karein
    weather_response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,apparent_temperature,"
                "precipitation,weather_code,wind_speed_10m"
            ),
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "auto",
            "forecast_days": 3
        },
        timeout=15
    )
    weather_response.raise_for_status()
    data = weather_response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})

    weather_names = {
        0: "Clear sky",
        1: "Mostly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Freezing fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Severe thunderstorm"
    }

    code = current.get("weather_code")
    current["description"] = weather_names.get(code, "Weather information")
    current["city"] = place["name"]
    current["country"] = place.get("country", "")
    current["timezone"] = data.get("timezone", "")

    forecast = []
    dates = daily.get("time", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    codes = daily.get("weather_code", [])

    for i in range(len(dates)):
        forecast.append({
            "date": dates[i],
            "high": highs[i],
            "low": lows[i],
            "description": weather_names.get(codes[i], "Weather information")
        })

    return {"current": current, "forecast": forecast}, None


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = "Multan"

    if request.method == "POST":
        city = request.form.get("city", "").strip()

    if city:
        try:
            weather, error = get_weather(city)
        except requests.RequestException:
            error = "API se rabta nahi ho saka. Internet check karke dobara koshish karein."
        except (KeyError, TypeError, ValueError):
            error = "Mausam ka data samajhne mein masla hua. Dobara koshish karein."

    return render_template("index.html", weather=weather, error=error, city=city)


if __name__ == "__main__":
    app.run(debug=True)
