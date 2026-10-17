
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException
)


# Chrome browser kholein
driver = webdriver.Chrome()

# Cookie Clicker ki experimental website
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Page ko load hone ka waqt dein
time.sleep(3)

# Cookie aur score ke elements dhoondein
cookie = driver.find_element(By.ID, "cookie")
score = driver.find_element(By.ID, "money")

# Game 60 seconds chalegi
end_time = time.time() + 60
next_purchase_time = time.time() + 5

while time.time() < end_time:

    # Cookie par click karein
    cookie.click()

    # Har 5 seconds baad upgrade khareedne ki koshish
    if time.time() >= next_purchase_time:

        try:
            # Products ki prices parhein
            products = driver.find_elements(
                By.CSS_SELECTOR,
                "#store div"
            )

            affordable_products = []

            for product in products:
                try:
                    product_id = product.get_attribute("id")

                    # Sirf numbered products select karein
                    if not product_id.startswith("product"):
                        continue

                    if not product_id[7:].isdigit():
                        continue

                    if product.get_attribute("class") == "grayed":
                        continue

                    affordable_products.append(product)

                except (NoSuchElementException, AttributeError):
                    continue

            # Sab se mehnga available product pehle khareedein
            if affordable_products:
                affordable_products[-1].click()

        except (NoSuchElementException, WebDriverException):
            print("Upgrade abhi nahi khareeda ja saka.")

        next_purchase_time = time.time() + 5

# Final score dikhayein
print("Final cookies:", score.text)
print("Game complete!")

# Browser khula rehne dein taa-ke aap result dekh sakein
input("Browser band karne ke liye Enter dabayein...")
driver.quit()
