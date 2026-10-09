import requests

# Aapki API Key
API_KEY = "e7b55f4141812f99910e12fa9c8ffcd3"

city = "Multan"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if data["cod"] == 200:
    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]
    print(f"{city} ka mausam: {weather}")
    print(f"Temperature: {temp}°C")
else:
    print("Error:", data["message"])