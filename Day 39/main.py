
# Day 39 - Flight Price Tracker
# API key aur Google Sheet ke baghair

destinations = [
    {"city": "Dubai", "price": 75000, "limit": 80000},
    {"city": "Istanbul", "price": 145000, "limit": 150000},
    {"city": "London", "price": 220000, "limit": 180000},
    {"city": "Doha", "price": 90000, "limit": 100000},
]

print("=" * 45)
print("       FLIGHT PRICE TRACKER")
print("=" * 45)

print("\nTicket prices ka muqabla:\n")

for destination in destinations:
    city = destination["city"]
    price = destination["price"]
    limit = destination["limit"]

    print(f"City: {city}")
    print(f"Ticket price: Rs. {price:,}")
    print(f"Your maximum budget: Rs. {limit:,}")

    if price <= limit:
        print("Status: Aap ke budget mein hai!")
    else:
        print("Status: Abhi ticket mehnga hai.")

    print("-" * 35)

cheapest = min(destinations, key=lambda item: item["price"])

print("\nSab se sasta ticket:")
print(f"City: {cheapest['city']}")
print(f"Price: Rs. {cheapest['price']:,}")

print("\nProgram complete!")
