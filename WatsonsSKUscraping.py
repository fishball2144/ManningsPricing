##import Library
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from datetime import date
from datetime import datetime
import time

# target url
target_url_list = [
    'https://www.watsons.com.hk/%E8%AD%B7%E8%88%92%E5%AF%B6radiant%E6%97%A5%E7%94%A824cm-9%E7%89%87/p/BP_287456', 'https://www.watsons.com.hk/%E6%BB%8B%E6%BD%A4%E8%82%B2%E9%AB%AE%E7%B2%BE%E8%8F%AF%E7%B4%A0/p/BP_266919']

# access url by using webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())


product_offer_list = []
targetProductdetail = []

# pop up message handler


def remove_popup():
    try:  # popup message handler
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "icon-close-button-1625037548411"))).click()
    except:
        print("no popup message!")


def get_product_data(target_url):
    r = driver.get(target_url)
    remove_popup()
    time.sleep(0.2)
    # web element locator
    productName = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[2]/e2-product-summary/h1').text
    productBrand = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[2]/e2-product-summary/h2/a').text
    productPrice = driver.find_element_by_class_name('displayPrice').text
    productOffer = driver.find_elements_by_class_name('tab')
    productId = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[13]/e2-product-code/p/span').text

    for offer in productOffer:
        product_offer_list.append(offer.text)

    print(productName)
    print(productBrand)
    print(productPrice)
    print(productId)
    print(product_offer_list)

    ItemDetails = {
        'product Name': productName,
        'Brand': productBrand,
        'Price': productPrice,
        'WAT Product ID': productId,
        'Product Offer': product_offer_list,
        'Record Time': date.today()
    }
    targetProductdetail.append(ItemDetails)


for url in target_url_list:
    get_product_data(url)

print(targetProductdetail)

# use pandas to create dataframe and export to excel or csv
df = pd.DataFrame(targetProductdetail)
datestring = datetime.strftime(date.today(), ' %d%m%Y')
# df.to_csv('product_detail.csv')
df.to_excel('Watsons product_detail'+datestring+'.xlsx')
print('saved to file')

# close the webdriver after finish all
driver.quit()
