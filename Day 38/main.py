import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# User se input lena
exercise_text = input("Aaj aap ne kaunsi exercise ki? Misal: I ran for 30 minutes: ")

# Nutritionix API try karna
try:
    nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        "x-app-id": os.getenv("NUTRITIONIX_APP_ID"),
        "x-app-key": os.getenv("NUTRITIONIX_API_KEY"),
    }
    params = {
        "query": exercise_text,
        "gender": os.getenv("GENDER"),
        "weight_kg": os.getenv("WEIGHT_KG"),
        "height_cm": os.getenv("HEIGHT_CM"),
        "age": os.getenv("AGE"),
    }
    response = requests.post(nutritionix_endpoint, json=params, headers=headers)
    response.raise_for_status()
    result = response.json()["exercises"][0]
    exercise_name = result["name"]
    duration = result["duration_min"]
    calories = result["nf_calories"]
except Exception as e:
    print(f"API se rabta karte waqt masla hua, lekin fikar nahi, hum dummy data se kaam chalayenge. Error: {e}")
    # Agar API fail ho jaye to dummy data
    exercise_name = "Running"
    duration = 30
    calories = 350

# Ab Sheety par bhejna
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
sheety_headers = {
    "Authorization": f"Bearer {os.getenv('SHEETY_TOKEN')}"
}

sheety_params = {
    os.getenv("SHEETY_ROW_KEY", "workout"): {
        "date": today_date,
        "time": now_time,
        "exercise": exercise_name.title(),
        "duration": duration,
        "calories": calories,
    }
}

sheety_response = requests.post(sheety_endpoint, json=sheety_params, headers=sheety_headers)
print(sheety_response.text)
print("Ho gaya! Data Sheet mein chala gaya hai.")