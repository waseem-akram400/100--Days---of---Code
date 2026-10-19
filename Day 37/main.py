
import os
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")
GRAPH_ID = os.getenv("PIXELA_GRAPH_ID", "walking")

BASE_URL = "https://pixe.la/v1/users"

headers = {
    "X-USER-TOKEN": TOKEN or ""
}


def create_graph():
    url = f"{BASE_URL}/{USERNAME}/graphs"

    graph_config = {
        "id": GRAPH_ID,
        "name": "Walking Tracker",
        "unit": "minute",
        "type": "int",
        "color": "shibafu"
    }

    response = requests.post(
        url,
        json=graph_config,
        headers=headers,
        timeout=20
    )

    print("Create graph:", response.text)


def add_today_pixel(minutes):
    today = datetime.datetime.now().strftime("%Y%m%d")

    url = f"{BASE_URL}/{USERNAME}/graphs/{GRAPH_ID}"

    pixel_data = {
        "date": today,
        "quantity": str(minutes)
    }

    response = requests.post(
        url,
        json=pixel_data,
        headers=headers,
        timeout=20
    )

    print("Add record:", response.text)


def update_today_pixel(minutes):
    today = datetime.datetime.now().strftime("%Y%m%d")

    url = (
        f"{BASE_URL}/{USERNAME}/graphs/"
        f"{GRAPH_ID}/{today}"
    )

    response = requests.put(
        url,
        json={"quantity": str(minutes)},
        headers=headers,
        timeout=20
    )

    print("Update record:", response.text)


def delete_today_pixel():
    today = datetime.datetime.now().strftime("%Y%m%d")

    url = (
        f"{BASE_URL}/{USERNAME}/graphs/"
        f"{GRAPH_ID}/{today}"
    )

    response = requests.delete(
        url,
        headers=headers,
        timeout=20
    )

    print("Delete record:", response.text)


if __name__ == "__main__":
    if not USERNAME or not TOKEN:
        print("Please add your Pixela username and token to .env.")
    else:
        print("1. Create graph")
        print("2. Add today's walking record")
        print("3. Update today's record")
        print("4. Delete today's record")

        choice = input("Choose 1, 2, 3, or 4: ")

        if choice == "1":
            create_graph()
        elif choice == "2":
            minutes = int(input("How many minutes did you walk today? "))
            add_today_pixel(minutes)
        elif choice == "3":
            minutes = int(input("Enter the updated walking minutes: "))
            update_today_pixel(minutes)
        elif choice == "4":
            confirm = input("Delete today's record? Type YES: ")
            if confirm == "YES":
                delete_today_pixel()
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid choice.")
