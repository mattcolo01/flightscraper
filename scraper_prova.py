from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('log-level=3')
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless=new')
chrome_options.add_argument("--incognito")
chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe', options=chrome_options )
driver.get("https://www.ryanair.com/it/it")
print(driver.current_url)

driver.find_element(By.CLASS_NAME, "cookie-popup-with-overlay__button").click()

departure="2023-05-10"
arrival="2023-05-17"

#%%

airport_code="BCN"
destination = driver.find_element(By.ID, "input-button__destination")
destination.click()
destination.send_keys(airport_code)
time.sleep(1)
driver.find_element(By.XPATH, '//span[@data-id = "{}"]'.format(airport_code) ).click()

#%%

#driver.find_element(By.XPATH, '//div[text() = " Scegli la data "]').click()
#today = driver.find_element(By.CLASS_NAME, "calendar-body__cell--today").text
time.sleep(1)
driver.find_element(By.XPATH, '//div[@data-id= "{}"]'.format(departure)).click()
driver.find_element(By.XPATH, '//div[@data-id= "{}"]'.format(arrival)).click()
#time.sleep(1)
driver.find_element(By.XPATH, '//span[text() = "Cerca"]').click()

#%%
costs = []
days = []

while len(costs)<2 :
    costs_tmp = driver.find_elements(By.CLASS_NAME, "price__integers")
    for c in costs_tmp:
        costs.append(c.text)
    days_tmp = driver.find_elements(By.CLASS_NAME, "date-item__day-of-month")
    for d in days_tmp:
        days.append(d.text)
    
#%%

print("To {}".format(airport_code))
for i in range(0,5):
    print( "Day {}: €{}".format(days[i], costs[i]) )
print("From {}".format(airport_code))
for i in range(5,10):
    print( "Day {}: €{}".format(days[i], costs[i]) )