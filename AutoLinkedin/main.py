from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


LOGIN = LINKEDIN_LOGIN
PASSWORD = LINKEDIN_PASSWORD

chrome_driver_path = "D:/DevPy/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=111154941&keywords=frontend&location=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F")

buttonLogin = driver.find_element(by=By.CSS_SELECTOR,value="body > div.base-serp-page > header > nav > div > a.nav__button-secondary")
buttonLogin.click()
time.sleep(5)

sendUsername = driver.find_element(by=By.ID,value="username")
sendUsername.send_keys(LOGIN)

sendPassword = driver.find_element(by=By.ID,value="password")
sendPassword.send_keys(PASSWORD)

button = driver.find_element(by=By.CSS_SELECTOR,value="#organic-div > form > div.login__form_action_container > button")
button.click()
time.sleep(10)

dataLi = driver.find_element(by=By.XPATH,value='/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul')
li = dataLi.find_elements(by=By.CLASS_NAME,value='jobs-search-results__list-item')

for i in range (1,len(li)+1):
    el  = driver.find_element(by=By.XPATH,value=f'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{str(i)}]')
    webdriver.ActionChains(driver).move_to_element(el).perform()

def update_page():
    listData = driver.find_elements(by=By.CSS_SELECTOR,value=".job-card-list__title")
    links= {}
    for i in range (len(listData)):
        links[i] = { "Text":listData[i].text, "Link":listData[i].get_attribute("href"),
                     "Element": listData[i]}
    return links

links = update_page()

print(links)

for i in range (len(links)):
    links[i]["Element"].click()

    try:
        job_button = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button.jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view"))).get_attribute("class")
    except:
        continue
    time.sleep(1)
    if "artdeco-button--icon-right" not in job_button:
        resume = driver.find_element(By.CSS_SELECTOR,value="button.jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
        resume.click()
        time.sleep(1)
        try:
            check_button = driver.find_element(by=By.XPATH,
                                               value="/html/body/div[3]/div/div/div[2]/div/form/footer/div[2]/button")
        except:
            check_button = driver.find_element(by=By.XPATH,
                                               value="/html/body/div[3]/div/div/div[2]/div/form/footer/div[3]/button")
        if check_button.get_attribute("aria-label") == "Отправить заявку":

            # number_phone_select = Select(driver.find_element(by=By.XPATH,value="/html/body/div[3]/div/div/div[2]/div/form/div/div/div[3]/div[1]/div/select"))
            # number_phone_select.select_by_value("urn:li:country:ru")
            #
            # number_phone = driver.find_element(by=By.TAG_NAME,value="input")
            # number_phone.send_keys("9851472466")
            try:
                next_page_resume = driver.find_element(by=By.XPATH,value="/html/body/div[3]/div/div/div[2]/div/form/footer/div[3]/button")
            except:
                next_page_resume = driver.find_element(by=By.XPATH,value="/html/body/div[3]/div/div/div[2]/div/form/footer/div[2]/button")
            next_page_resume.click()
            WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.artdeco-modal.artdeco-modal--layer-default button")))
            time.sleep(5)
            driver.find_element(by=By.CSS_SELECTOR,value=".artdeco-modal--layer-default button").click()
            links = update_page()
        else:
            driver.find_element(by=By.CSS_SELECTOR,value="button.artdeco-modal__dismiss").click()
            driver.find_element(by=By.XPATH,value="/html/body/div[3]/div[2]/div/div[3]/button[1]").click()
