
import csv
from pathlib import Path


# Practice data: sample property listings
properties = [
    {
        "price": "$1,500 per month",
        "address": "123 Main Street",
        "link": "https://example.com/property/1",
    },
    {
        "price": "$2,000 per month",
        "address": "45 Park Avenue",
        "link": "https://example.com/property/2",
    },
    {
        "price": "$1,250 per month",
        "address": "78 Lake Road",
        "link": "https://example.com/property/3",
    },
]


def save_to_csv(property_list):
    file_path = Path(__file__).parent / "properties.csv"

    fieldnames = ["price", "address", "link"]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(property_list)

    print(f"Data saved successfully: {file_path}")


def main():
    print("Day 53 - Property Data Entry")
    print("----------------------------")

    for item in properties:
        print(
            f"Price: {item['price']} | "
            f"Address: {item['address']}"
        )

    save_to_csv(properties)


if __name__ == "__main__":
    main()
