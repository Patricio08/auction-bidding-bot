from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# replace these values
username_input = "<USERNAME>"
pwd_input = "<PASSWORD>"
auction_url = "<AUCTION_URL>"
max_bid_value = 1 # UPDATE MAX VALUE
countdown_wait_time = 10800 # UPDATE COUNTDOWN WAIT TIME (default is 3h before)

driver.get("https://vendas.portaldasfinancas.gov.pt/vendasat")

nif = driver.find_element(By.CSS_SELECTOR, 'label[for="tab2"]').click()

username = driver.find_element(By.ID, "username")
username.send_keys(username_input)

pwd = driver.find_element(By.ID, "password-nif")
pwd.send_keys(pwd_input + Keys.ENTER)

driver.get(auction_url)

wait = WebDriverWait(driver, countdown_wait_time)

try:
    # wait until last second
    wait.until(
        EC.text_to_be_present_in_element((By.ID, 'days'), 0) and
        EC.text_to_be_present_in_element((By.ID, 'hours'), 0) and
        EC.text_to_be_present_in_element((By.ID, 'minutes'), 0) and
        EC.text_to_be_present_in_element((By.ID, 'seconds'), 1)
    )
    
    print("Countdown reached the desired state: 0 days, 0 hours, 0 minutes, and 1 second!")

    # refresh button
    driver.find_element(By.ID, "btnRefresh").click()

    # get last bid and convert to float
    cash_value_element = driver.find_element(By.CLASS_NAME, "cash-licit")
    cash_value_text = cash_value_element.text
    cash_value = cash_value_text.replace('€', '').strip()
    cash_value_float = float(cash_value.replace(',', '.'))

    # max value cap
    if cash_value_float > max_bid_value:
        print(f"Cash value is greater than 10: {cash_value_float}. Exiting script.")
        driver.quit() 
        sys.exit()    

    # accept user terms
    driver.find_element(By.ID, "checkCondicoes").click()

    # insert bit +1€ and enter
    new_bid = cash_value_float + 1
    driver.find_element(By.ID, "inputLicit").send_keys(new_bid)

    # enter
    driver.find_element(By.ID, "btnLicit").click()

    # wait some millis more & confirm (needs testing)
    time.sleep(0.5)
    driver.find_element(By.ID, "btnConfirm").click()

except TimeoutException:
    print("The countdown did not reach the expected state within the timeout period.")

driver.quit()