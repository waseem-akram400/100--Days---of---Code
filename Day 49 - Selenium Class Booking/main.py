
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome browser ki settings
options = Options()

# Chrome ko normal window mein kholna
driver = webdriver.Chrome(options=options)

# Ek test website kholna
driver.get("https://www.python.org")

# Website ka title dekhna
print("Website Title:", driver.title)

# Browser band karna
driver.quit()
