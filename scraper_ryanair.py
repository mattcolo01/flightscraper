from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('log-level=3')
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless=new')
chrome_options.add_argument("--incognito")
chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

departure=input("Giorno di partenza (formato yyyy-mm-dd): ")
arrival=input("Giorno di ritorno (formato yyyy-mm-dd): ")
output_string=""

driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe', options=chrome_options )

airports_file = open("airport_codes.txt", "+r")

airports_list = airports_file.readlines()

#%%

for airport_code in airports_list:
    airport_code=airport_code[0:3]
    print("Searching " + airport_code )
    driver.get("https://www.ryanair.com/it/it")
    try:
        driver.find_element(By.CLASS_NAME, "cookie-popup-with-overlay__button").click()
    except NoSuchElementException:
        1+1
    
    destination = driver.find_element(By.ID, "input-button__destination")
    destination.click()
    destination.send_keys(airport_code)
    
    #time.sleep(1)
    #driver.find_element(By.XPATH, '//span[@data-id = "{}"]'.format(airport_code) ).click()
    tmp = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@data-id = "{}"]'.format(airport_code))))
    tmp.click()
    
    #driver.find_element(By.XPATH, '//div[text() = " Scegli la data "]').click()
    #today = driver.find_element(By.CLASS_NAME, "calendar-body__cell--today").text
    
    tmp = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@data-id= "{}"]'.format(departure) )))
    tmp.click()
    #time.sleep(1)
    #driver.find_element(By.XPATH, '//div[@data-id= "{}"]'.format(departure)).click()
    driver.find_element(By.XPATH, '//div[@data-id= "{}"]'.format(arrival)).click()
    #time.sleep(1)
    driver.find_element(By.XPATH, '//span[text() = "Cerca"]').click()
    
    costs = []
    days = []
    
    while len(costs)<2 :
        costs_tmp = driver.find_elements(By.CLASS_NAME, "price__integers")
        for c in costs_tmp:
            costs.append(c.text)
        days_tmp = driver.find_elements(By.CLASS_NAME, "date-item__day-of-month")
        for d in days_tmp:
            days.append(d.text)

    output_string += "To {}\n".format(airport_code)
    for i in range(0,5):
        output_string += "Day {}: €{}\n".format(days[i], costs[i])
    output_string += "From {}\n".format(airport_code)
    for i in range(5,10):
        output_string += "Day {}: €{}\n".format(days[i], costs[i])
    
airports_file.close()
print(output_string)

#%%

flight_prices_file = open("flight_prices.txt", "w")
flight_prices_file.write(output_string)
flight_prices_file.close()