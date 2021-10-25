##import Library
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from datetime import date
import time

# access url by using webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.mannings.com.hk/"  # example url
r = driver.get(url)

# import your interested SKU in Mannings Code
target_product_list = [572123, 433243]

# an list to record product details
targetProductdetail = []

# pop up message handler


def remove_popup():
    try:  # popup message handler
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "pdv4close"))).click()
    except:
        print("no popup message!")

# Main function to record the product details


def get_product_data(key):
    # acess the Mannings website and input the Mannings product id
    remove_popup()
    inputElement = driver.find_element_by_id('js-site-search-input')
    inputElement.send_keys(key)
    inputElement.submit()
    time.sleep(0.2)
    # web element locator
    productName = driver.find_element_by_class_name('product_name_pdp').text
    productBrand = driver.find_elements_by_class_name(
        'labelunder_pdp')[0].text
    productPrice = driver.find_element_by_class_name('price').text
    productId = driver.find_element_by_class_name('sku_code_new').text
    productOffer = driver.find_elements_by_class_name("pdp_offer_section")

    # record the offer if more than one
    productOffer_list = []

    for offer in productOffer:
        productOffer_list.append(offer.text)

    # Convert to dictionary
    ItemDetails = {
        'product Name': productName,
        'Brand': productBrand,
        'Price': productPrice,
        'Product ID': productId,
        'Product Offer': productOffer_list[::2],
        'Record Time': date.today()
    }
    targetProductdetail.append(ItemDetails)


# loop the target product list and send to record function
for item in target_product_list:
    get_product_data(item)

print(targetProductdetail)

# use pandas to create dataframe and export to excel or csv
df = pd.DataFrame(targetProductdetail)
# df.to_csv('product_detail.csv')
df.to_excel('product_detail.xlsx')
print('saved to file')

# close the webdriver after finish all
driver.quit()
