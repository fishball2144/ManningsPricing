from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from datetime import date
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.mannings.com.hk/"  # example url

r = driver.get(url)


def remove_popup():
    try:  # popup message handler
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "pdv4close"))).click()
    except:
        print("no popup message!")


remove_popup()
inputElement = driver.find_element_by_id('js-site-search-input')
inputElement.send_keys('572123')
inputElement.submit()
time.sleep(0.5)
productName = driver.find_element_by_class_name('product_name_pdp').text
productBrand = driver.find_elements_by_class_name(
    'labelunder_pdp')
productPrice = driver.find_element_by_class_name('price').text
productId = driver.find_element_by_class_name('sku_code_new').text
productOffer = driver.find_elements_by_class_name(
    "pdp_offer_section")

productOffer_list = []
productBrand_list = []

for brand in productBrand:
    productBrand_list.append(brand.text)
for offer in productOffer:
    productOffer_list.append(offer.text)

print(productName)
print(productBrand_list[0])
print(productPrice)
print(productId)
print(productOffer_list)

driver.quit()
