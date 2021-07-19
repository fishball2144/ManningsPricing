from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

#url = "https://www.mannings.com.hk/personalcarenhair/personal-care/sanitary-protection/c/fesanitaryprotection"

url = input("what do you want to check?Please start from the first page!")

r = driver.get(url)

# driver.maximize_window()

try:  # popup message handler
    close_popup = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "pdv4close"))).click()
except:
    print("no popup message!")

product_offer_list = []
product_price_list = []
product_list = []
product_id_list = []
condition = True
while condition:
    productInfoList = driver.find_elements_by_class_name("product_content")
    for el in productInfoList:
        products = driver.find_elements_by_css_selector("h2.prod_description")
        product_prices = driver.find_elements_by_css_selector("p.price")
        product_offers = driver.find_elements_by_xpath(
            "//div[@class='offer_section']/span[@class='hidden-xs']")
    for product in products:
        product_list.append(product.text)
    for pp in product_prices:
        product_price_list.append(pp.text)
    for po in product_offers:
        product_offer_list.append(po.text)
    try:
        driver.find_element_by_xpath(
            "//li[@class='pagination-next']/a").click()  # go to next page
    except:
        condition = False
print(product_id_list)

pricing = list(zip(product_list, product_price_list, product_offer_list))
print(pricing)
data = pd.DataFrame(pricing)
data.to_excel("pricing_data.xlsx", index=False)
