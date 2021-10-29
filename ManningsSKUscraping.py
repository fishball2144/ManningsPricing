# import Library
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import os
from datetime import date
from datetime import datetime
import pathlib
import time

# access url by using webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.mannings.com.hk/"  # example url
r = driver.get(url)

# import your interested SKU in Mannings Code
# can also index sheet by name or fetch all sheets
df = pd.read_excel('target.xlsx', sheet_name='MAN product',converters={'MAN ID':str})
target_list = df['MAN ID'].tolist()

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


def garfield():
    try:
        garfieldPromotion = driver.find_element_by_class_name(
            'garfield_mannings_pdp')
    except:
        return 'False'
    return 'True'


def get_product_data(key):
    # acess the Mannings website and input the Mannings product id
    remove_popup()
    inputElement = driver.find_element_by_id('js-site-search-input')
    inputElement.send_keys(key)
    inputElement.submit()
    # time.sleep(0.2)
    # web element locator
    productName = driver.find_element_by_class_name('product_name_pdp').text
    productBrand = driver.find_elements_by_class_name(
        'labelunder_pdp')[0].text
    productPrice = driver.find_element_by_class_name('price').text
    productId = driver.find_element_by_class_name('sku_code_new').text
    productOffer = driver.find_elements_by_class_name("pdp_offer_section")
    isGarfield = garfield()
    # record the offer if more than one
    productOffer_list = []

    for offer in productOffer:
        productOffer_list.append(offer.text)

    if any(str.format("20%off") in od for od in productOffer_list):
        promotionProductPrice = float(productPrice.replace('$', ''))*0.8
    elif any(str.format("10%off") in od for od in productOffer_list):
        promotionProductPrice = float(productPrice.replace('$', ''))*0.9
    elif any(str.format("15%off") in od for od in productOffer_list):
        promotionProductPrice = float(productPrice.replace('$', ''))*0.85
    elif any(str.format("30%off") in od for od in productOffer_list):
        promotionProductPrice = float(productPrice.replace('$', ''))*0.7
    elif any(str.format("2nd pc 50% off") in od for od in productOffer_list):
        promotionProductPrice = float(productPrice.replace('$', ''))*0.75
    elif any(str.format("Buy 1 Get 1 Free") in od for od in productOffer_list):
        promotionProductPrice = float(productPrice.replace('$', ''))*0.5
    else:
        promotionProductPrice = productPrice.replace('$', '')

    # Convert to dictionary
    ItemDetails = {
        'product Name': productName,
        'Brand': productBrand,
        'Price': productPrice.replace('$', ''),
        'Promotion Price': promotionProductPrice,
        'MAN Product ID': productId,
        'Garfield Promotion': isGarfield,
        'Product Offer': '\n'.join(productOffer_list[::2]),
        'Record Time': date.today()
    }
    targetProductdetail.append(ItemDetails)


# loop the target product list and send to record function
for item in target_list:
    get_product_data(item)

print(targetProductdetail)
script_path = os.path.dirname(os.path.abspath(__file__))
# use pandas to create dataframe and export to excel or csv
pathlib.Path(script_path+'\\record').mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(targetProductdetail)
datestring = datetime.strftime(date.today(), ' %d%m%Y')
# df.to_csv('product_detail.csv')
print(script_path+'/record/Mannings product_detail')
df.to_excel(script_path+'\\record\\Mannings product_detail'+datestring+'.xlsx')

print('saved to file')

# close the webdriver after finish all
driver.quit()
