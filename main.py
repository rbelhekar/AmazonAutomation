from selenium import webdriver
from selenium.common import TimeoutException
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
wait = WebDriverWait(driver,10) # explicit wait for 10 seconds
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
first_product = driver.find_element(By.CSS_SELECTOR,"a.a-link-normal>h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")
print(f"First Product : {first_product.text}")

# Locating all listed products
print("Finding all products in all pages.")

# Print before starting the loop
print("-"*40)
print("AMAZON LAPTOP SALE")

# Prepare CSV
csv_headers = ["Product","Price","Rating","Reviews","Link"]
file_name = "AMAZON_LAPTOPS.csv"

# Open/Create CSV
with (open(file_name, mode="w", newline="", encoding="utf-8") as file):
    writer = csv.writer(file)
    writer.writerow(csv_headers)
    while True:

        listed_products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a.a-link-normal>h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")))
        for idx,product in enumerate(listed_products):
            # ✅ Scroll into view to force lazy loading
            #driver.execute_script("arguments[0].scrollIntoView(true);", product)
            #time.sleep(0.5)  # Small pause to let content load
            # Product name
            product_name = product.text.strip()

            # Find Price
            try :
                price_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.puisg-col-inner>div.a-section>div.a-row>div.a-row>a.a-link-normal>span.a-price")))[idx]
                price = price_element.text.strip()
            except :
                price = "N/A"

            # Find Rating
            try :
                rating_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.puisg-col-inner>div.a-section>div.a-section>div.a-row.a-size-small>span.a-declarative>a.a-declarative")))[idx]
                rating = rating_element.get_attribute("aria-label").strip()[:3]
            except :
                rating = "N/A"

            # Find Reviews count
            try:
                reviews_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.puisg-col-inner>div.a-section>div.a-section>div.a-row.a-size-small>a.a-link-normal>span.a-size-base")))[idx]
                reviews = reviews_element.text.strip()
            except:
                reviews = "N/A"

            # Find Links
            try:
                url_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.puisg-col-inner>div.a-section>div.a-section>a.a-link-normal")))[idx]
                url = url_element.get_attribute("href")
            except:
                url = "N/A"

            # Write data to CSV
            writer.writerow([product_name,price,rating,reviews,url])
            print(f"Product : {product_name}")
            print(f"Price : {price}")
            print(f"Rating : {rating}")
            print(f"Reviews : {reviews}")
            print(f"URL : {url}")
            print("-"*40)

        # Get Pagination Next button
        try :
            pagination_next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.s-pagination-next")))
            pagination_next_button.click()
            time.sleep(0.5)
        except TimeoutException :
            break

# Close the browser
print("Closing browser.")
driver.close()