import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pprint

HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Accept-Language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6"
}

content = requests.get(url="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
                       headers=HEADERS)

bs = BeautifulSoup(content.text, "html.parser")

blocks_list = bs.find_all(class_="photo-cards")[0].find_all('li')


dict_houses = {}

for i in range(len(blocks_list)):
    try:

        dict_houses[i] = {"price":''.join([j for j in blocks_list[i].select_one('span').getText().replace('$','').split(' ')[0] if  j.isdigit()]),
                          "address" :blocks_list[i].find_next(name='address').getText(),
                          "link": blocks_list[i].find_next(name='a').get('href') if 'https' in  blocks_list[i].find_next(name='a').get('href') else "https://www.zillow.com" + blocks_list[i].find_next(name='a').get('href')  }

    except:

        continue


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://docs.google.com/forms/d/e/1FAIpQLScbPwW_jhOFGz4j3pmUx_4CXSbLn6NWaZbAgFF11dQrEocesw/viewform?fbzx=5668324248468671186")
time.sleep(2)
for i in dict_houses:
    address = driver.find_element(by=By.XPATH,value="//span[text()=\"What's the address of the property?\"]/../../../..//input")
    logging.warning(f"ADDRESS:{address}")
    address.send_keys(dict_houses[i]["address"])
    price = driver.find_element(by=By.XPATH,
                                  value="//span[text()=\"What's the price per month?\"]/../../../..//input")
    price.send_keys(dict_houses[i]["price"])
    logging.warning(f"PRICE:{price}")

    link = driver.find_element(by=By.XPATH,
                                  value="//span[text()=\"What's the link of the property?\"]/../../../..//input")
    link.send_keys(dict_houses[i]["link"])
    logging.warning(f"LINK:{link}")

    send_button = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    send_button.click()
    send_again = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
    send_again.click()

while True:
    pass
