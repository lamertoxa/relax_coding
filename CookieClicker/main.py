import time

start_time = time.time()
cooldown = start_time

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://orteil.dashnet.org/experiments/cookie/")
button =  driver.find_element(by=By.ID,value='cookie')



def choice():
    for i in list_things:
        new_value = driver.find_element(by=By.ID, value=i)
        if new_value.get_attribute("class") != "grayed" and list_things.index(i)!=0:
            if int(driver.find_element(by=By.XPATH,
                value=f'//*[@id="{i}"]/b').text.split("-")[1].replace(",","")
            ) >= int(driver.find_element(by=By.XPATH,
                value=f'//*[@id="{list_things[list_things.index(i)-1]}"]/b'
                      f'').text.split("-")[1].replace(",",""))//2:
                list_things.remove(i)
                continue
            return new_value

list_things = ["buyTime machine", "buyPortal", "buyAlchemy lab", "buyShipment",
               "buyMine", "buyFactory", "buyGrandma"]



while True:
    if  int(time.time())-int(start_time) >= 300:
        print(driver.find_element(by=By.ID,value="cps").text)
        break
    if int (time.time())-int(cooldown) >=5:

        element = choice()
        if element is not None:
            element.click()
        cooldown = time.time()


    button.click()



