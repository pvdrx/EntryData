import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep

CHROME_DRIVER_PATH = "Your driver location"
s = Service(CHROME_DRIVER_PATH)

form_url = "https://docs.google.com/forms/d/e/1FAIpQLScZIQRsYGMztwXDjf3xxo3ql0wQZKYd3cfslV-YNths53Nh1A/viewform"

zillow_url = "https://www.zillow.com/san-francisco-ca/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D" \
             "%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122" \
             ".536739%2C%22east%22%3A-122.32992%2C%22south%22%3A37.707608%2C%22north%22%3A37.842914%7D%2C" \
             "%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22" \
             "%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A683460%7D%2C%22mp%22%3A" \
             "%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22" \
             "%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore" \
             "%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22" \
             "%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C" \
             "%22isListVisible%22%3Atrue%7D "

header = {"Accept-Language": "en-US,en;q=0.9",
          "User-Agent": "Your user agent"}

response = requests.get(zillow_url, headers=header)

website = response.text

soup = BeautifulSoup(website, "html.parser")

all_address = soup.find_all("address", attrs={"data-test": "property-card-addr"})
address_list = [address.get_text() for address in all_address]
# print(address_list)

prices = soup.find_all("span", attrs={"data-test":"property-card-price"})
prices_list = [price.get_text() for price in prices]
clean_prices = [numbers.replace("/", "").replace("+ 1 bd", "").replace("mo", "").replace("+", "")
                for numbers in prices_list]
# print(clean_prices)

links = []
for a in soup.find_all('a', class_="StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 dZxoFm"
                                   " property-card-link", href=True):
    if "/b/" in a["href"]:
        links.append(f"https://www.zillow.com{a['href']}")
    else:
        links.append(a['href'])

# print(links)

driver = webdriver.Chrome(service=s)

sleep(5)

cont = 0

for answer in address_list:
    driver.get(form_url)
    sleep(8)
    address_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/'
                                                 'div[2]/div/div[1]/div/div[1]/input')
    price_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/d'
                                               'iv[2]/div/div[1]/div/div[1]/input')
    link_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/di'
                                              'v[2]/div/div[1]/div/div[1]/input')
    send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_form.send_keys(address_list[cont])
    price_form.send_keys(clean_prices[cont])
    link_form.send_keys(links[cont])
    sleep(2)
    send_button.click()
    sleep(3)
    cont += 1
