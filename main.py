from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os
import re

# env reading:
load_dotenv()

print('Reading password...')
myki_username = os.getenv("MYKI_USERNAME")
myki_password = os.getenv("MYKI_PASSWORD")

if not myki_username or not myki_password:
    print("Error: Please set the MYKI_USERNAME and MYKI_PASSWORD in the .env file.")
    exit()


# Set up ChromeDriver
chrome_driver_path = r"chromedriver/chromedriver.exe"

print('starting browser...')
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)

print('loading myki webpage...')
driver.get("https://www.ptv.vic.gov.au/tickets/myki")

time.sleep(3)

# Find the login fields 
print('logging in...')
username_field = driver.find_element(By.ID, "loginUsername")  # replace with actual ID if different
password_field = driver.find_element(By.ID, "loginPassword")  # replace with actual ID if different

# enters the password and username.
username_field.send_keys(myki_username)
password_field.send_keys(myki_password)

# Submit the form 
password_field.send_keys(Keys.RETURN)
try:
    time.sleep(2)
    error_message_element = driver.find_element(By.CLASS_NAME, 'myki-form__error-content')
    print(error_message_element.text)
except:
    print('login successful'
          )
time.sleep(5)

# get myki details:
try:
    cardName = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'myki-card__card-holder__name'))
    )
        
    mykiBalance = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'myki-card__myki-money__current'))
    )
    mykiNumber = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'myki-card__card-holder__myki-number'))
    )
    
    def format_myki_text(text):
        # Remove newlines and extra spaces
        text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()
        
        # Check for "Mobile myki" or "{name}'s myki"
        if "Mobile myki" in text:
            text = text.replace("Mobile myki", "mobile myki")
        else:
            text = text.replace("myki", "myki")
        
        # Extract name and number if present
        name_match = re.search(r"\{name\}", text)
        number_match = re.search(r"\{number\}", text)
        
        if number_match:
            text = text.replace("{number}", number_match.group())
        
        return text
        
    for index, (name_element, balance_element, number_element) in enumerate(zip(cardName, mykiBalance, mykiNumber)):
        name_text = name_element.text
        balance_text = balance_element.text
        cardNumber = number_element.text
        
        # cause it sends it like 'Last known balance $4.70,$4.70'
        parts = balance_text.split(',')
        balance_text = parts[1].strip() if len(parts) > 1 else ''
        
        
        print(f"Myki {index + 1}: {format_myki_text(name_text)} - Balance: {balance_text}")



except Exception as e:
    print(f'no myki details found\nError: {e}')

driver.quit()
