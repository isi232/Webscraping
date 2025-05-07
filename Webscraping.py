from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

def extract_digits(text):
    return ''.join([ch for ch in text if ch in "0123456789"])

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://tap.az/elanlar/transport/cars/mercedes"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

wb = Workbook()
ws = wb.active
ws.title = "Mercedes Qiymetler"
ws.append(["Title", "Price"])

products = soup.find_all("div", class_="products-i__info")

for product in products:
    title_tag = product.find("div", class_="products-i__name")
    price_tag = product.find("div", class_="products-i__price")

    title = title_tag.get_text(strip=True) if title_tag else ""
    raw_price = price_tag.get_text(strip=True) if price_tag else ""
    price = extract_digits(raw_price)

    if price:
        try:
            price_value = int(price)
            if 20000 <= price_value <= 30000:
                ws.append([title, price])
        except ValueError:
            continue

wb.save("tapaz_mercedes_qiymetler_20k_30k.xlsx")
print("Hazırdır: tapaz_mercedes_qiymetler_20k_30k.xlsx")
