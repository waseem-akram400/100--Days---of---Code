class CoffeeMachine:

    def __init__(self):
        # Resources جو مشین میں ہیں
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100
        }

        # رقم جو اکٹھی ہوئی
        self.money = 0

        # مشین کی حالت
        self.is_on = False

        # کافی کی مینو
        self.menu = {
            "espresso": {"water": 50, "milk": 0, "coffee": 18, "price": 1.5},
            "latte": {"water": 200, "milk": 150, "coffee": 24, "price": 2.5},
            "cappuccino": {"water": 250, "milk": 100, "coffee": 24, "price": 3.0}
        }

    def turn_on(self):
        self.is_on = True
        print("☕ Welcome to Coffee Machine!")

    def turn_off(self):
        self.is_on = False
        print("Thank you! Goodbye!")

    def display_menu(self):
        print("\n" + "=" * 40)
        print("MENU")
        print("=" * 40)
        for coffee, details in self.menu.items():
            print(f"{coffee.upper()}: ${details['price']}")
        print("=" * 40)

    def check_resources(self, coffee_type):
        required = self.menu[coffee_type]

        for item, amount in required.items():
            if item != "price":
                if self.resources[item] < amount:
                    print(f"❌ Not enough {item}")
                    return False

        return True

    def process_payment(self, coffee_type):
        price = self.menu[coffee_type]["price"]
        print(f"Price: ${price}")

        try:
            payment = float(input("Enter payment: $"))

            if payment < price:
                print(f"❌ Insufficient funds!")
                return False

            elif payment > price:
                change = payment - price
                print(f"✅ Change: ${change:.2f}")

            self.money += price
            return True

        except ValueError:
            print("❌ Invalid input!")
            return False

    def make_coffee(self, coffee_type):
        required = self.menu[coffee_type]

        for item, amount in required.items():
            if item != "price":
                self.resources[item] -= amount

        print(f"☕ {coffee_type.upper()} is ready!")

    def show_resources(self):
        print("\nResources:")
        for item, amount in self.resources.items():
            print(f"  {item}: {amount}")

    def run(self):
        self.turn_on()

        while self.is_on:
            self.display_menu()
            user_input = input("Enter choice (or 'quit'): ").lower()

            if user_input == "quit":
                self.turn_off()
                break

            elif user_input == "resources":
                self.show_resources()

            elif user_input in self.menu:
                if self.check_resources(user_input):
                    if self.process_payment(user_input):
                        self.make_coffee(user_input)

            else:
                print("❌ Invalid choice!")


# ═══════════════════════════════════════════════════════════
# MAIN PROGRAM
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    machine = CoffeeMachine()
    machine.run()