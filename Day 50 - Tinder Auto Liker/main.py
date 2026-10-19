
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def main():
    # 1. Chrome browser ki settings
    options = Options()
    options.add_argument("--start-maximized")

    driver = None

    try:
        # 2. Chrome browser start karein
        driver = webdriver.Chrome(options=options)

        # 3. Test website kholein
        driver.get("https://www.selenium.dev/selenium/web/clicks.html")

        # 4. Website ka title print karein
        print("Website Title:", driver.title)

        # 5. Button ko us ke ID se dhoondein
        button = driver.find_element(By.ID, "overflow")

        # 6. Button par click karein
        button.click()

        # 7. Kamyabi ka paigham
        print("Button par click kamyabi se ho gaya!")

    except WebDriverException as error:
        print("Browser ya website mein masla aaya:")
        print(error)

    finally:
        # 8. Kaam khatam hone par browser band karein
        if driver is not None:
            driver.quit()
            print("Chrome browser band ho gaya.")


if __name__ == "__main__":
    main()
