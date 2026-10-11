
import csv
from pathlib import Path

FILE_NAME = Path(__file__).with_name("customers.csv")


def create_file():
    if not FILE_NAME.exists():
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Email"])


def add_customer():
    name = input("Apna naam likhein: ").strip()
    email = input("Apna email likhein: ").strip()

    if not name or "@" not in email or "." not in email:
        print("Naam ya email durust nahi.")
        return

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, email])

    print("Customer ka record save ho gaya!")


def show_customers():
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        customers = list(csv.DictReader(file))

    if not customers:
        print("Abhi koi customer mojood nahi.")
        return

    print("\nCustomer list:")

    for customer in customers:
        print(
            f"Name: {customer['Name']} | "
            f"Email: {customer['Email']}"
        )


def main():
    create_file()

    while True:
        print("\n--- FLIGHT CLUB ---")
        print("1. Naya customer add karein")
        print("2. Customers ki list dekhein")
        print("3. Program band karein")

        choice = input("Apna intikhab likhein (1, 2, 3): ").strip()

        if choice == "1":
            add_customer()
        elif choice == "2":
            show_customers()
        elif choice == "3":
            print("Program band ho gaya.")
            break
        else:
            print("Sirf 1, 2 ya 3 likhein.")


if __name__ == "__main__":
    main()
