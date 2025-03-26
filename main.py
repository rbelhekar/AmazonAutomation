from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


# Start Chrome Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Open Amazon website
driver.get("https://www.amazon.in")
wait = WebDriverWait(driver,20) # explicit wait for 10 seconds
print("Amazon website is now opened for testing.")

# Locate search text box element and enter "laptop" in it
search_textbox = driver.find_element(By.ID,"twotabsearchtextbox")
search_textbox.send_keys("laptop")
time.sleep(0.5)

# Locate the search button and click on it
search_button = driver.find_element(By.ID,"nav-search-submit-button")
search_button.click()
time.sleep(1)

# Locate the first product
print("Finding first product.")
first_product = driver.find_element(By.CSS_SELECTOR,"h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
print(f"First Product : {first_product.text}")

# Locating all listed products
print("Finding all products and their prices.")
all_listed_products = driver.find_elements(By.CSS_SELECTOR,"h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
# all_listed_prices = driver.find_elements(By.CSS_SELECTOR,"span.a-price")
print("Amazon Laptop Products : ")
csv_headers = ["Product","Price"]
file_name = "exported_data.csv"
with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)
    for idx,product in enumerate(all_listed_products):
        price_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"span.a-price")))[idx]
        price = price_element.text.strip()
        writer.writerow([product.text,price])
        print(f"Product : {product.text}")
        print(f"Price : {price}")
        print("-"*40)

# Close the browser
print("Closing browser.")
driver.close()