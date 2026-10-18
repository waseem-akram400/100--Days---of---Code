
import os
import smtplib
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText


# .env file se settings parhein
load_dotenv()

# Apne product ka URL yahan dein
PRODUCT_URL = os.getenv("PRODUCT_URL", "")

# Is price se kam hone par alert bhejna hai
BUY_PRICE = float(os.getenv("BUY_PRICE", "100"))

# Browser jaisi request bhejne ke liye headers
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}


def get_product_price():
    """Amazon page se product ki price hasil karne ki koshish."""

    if not PRODUCT_URL:
        print("ERROR: .env file mein PRODUCT_URL add karein.")
        return None

    try:
        response = requests.get(
            PRODUCT_URL,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Amazon ke aam price selectors
        price_element = (
            soup.select_one("span.a-price span.a-offscreen")
            or soup.select_one("#priceblock_ourprice")
            or soup.select_one("#priceblock_dealprice")
        )

        if price_element is None:
            print("Price nahi mili. Amazon ne page badla ya access roki.")
            return None

        price_text = price_element.get_text(strip=True)
        price_text = (
            price_text.replace(",", "")
            .replace("$", "")
            .replace("£", "")
            .replace("€", "")
        )

        price = float(price_text)

        print(f"Current price: {price}")
        return price

    except (requests.RequestException, ValueError) as error:
        print("Price hasil karne mein masla:", error)
        return None


def send_email(price):
    """Price kam hone par email bhejne ki koshish."""

    sender = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not app_password or not receiver:
        print("Email settings .env file mein mukammal nahi hain.")
        return

    message = MIMEText(
        f"Product ki current price {price} hai. "
        f"Aap ki target price {BUY_PRICE} hai."
    )

    message["Subject"] = "Amazon Price Alert"
    message["From"] = sender
    message["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, app_password)
            server.send_message(message)

        print("Email alert successfully bhej diya gaya!")

    except (smtplib.SMTPException, OSError) as error:
        print("Email bhejne mein masla:", error)


# Main program
current_price = get_product_price()

if current_price is not None:
    if current_price < BUY_PRICE:
        print("Price target se kam hai!")
        send_email(current_price)
    else:
        print("Abhi price target se kam nahi hui.")
else:
    print("Price check nahi ho saka.")
