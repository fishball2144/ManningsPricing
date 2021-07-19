from selenium import webdriver
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.mannings.com.hk/personalcarenhair/personal-care/sanitary-protection/c/fesanitaryprotection"

r = driver.get(url)

try:
    close_popup = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.ID, "pdv4close"))).click()
except:
    print("no popup message!")

driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
products = driver.find_elements_by_css_selector(
    "h2.prod_description")
product_prices = driver.find_elements_by_css_selector("p.price")
product_offers = driver.find_elements_by_xpath(
    "//div[@class='offer_section']/span[@class='hidden-xs']")

for product in products:
    print(product.text)

for product_price in product_prices:
    print(product_price.text)

for product_offer in product_offers:
    print(product_offer.text)
