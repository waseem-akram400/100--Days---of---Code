from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# HTML file ka poora path hasil karein
html_file = Path(__file__).with_name("form.html").resolve().as_uri()

# Browser kholein
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

try:
    print("Automation shuru ho rahi hai...")

    # Apna local test form kholein
    driver.get(html_file)

    # Form ke fields dhoondein
    name_field = wait.until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    email_field = driver.find_element(By.ID, "email")
    submit_button = driver.find_element(By.ID, "submit")

    # Form mein test information bharein
    name_field.send_keys("Python Student")
    email_field.send_keys("student@example.com")

    print("Form fill ho gaya.")

    # Submit button par click karein
    submit_button.click()

    # Success message ka intezar karein
    message = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    print("Success:", message.text)
    print("Automation successfully complete ho gayi!")

except Exception as error:
    print("Automation mein masla aaya:", error)
    raise

finally:
    # Natija dekhne ke liye browser 5 seconds baad band hoga
    import time
    time.sleep(5)
    driver.quit()
