import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import uuid
from time import sleep
from dotenv import load_dotenv
import os
from flask import Flask

load_dotenv()

app = Flask(__name__)

app.config['mongodb_url'] = os.getenv('MONGODB_URI')
app.config['email'] = os.getenv('email')
app.config['password'] = os.getenv('password')

print(app.config['email'])

client = MongoClient(app.config['mongodb_url'])
db = client["twitter_trends"]
collection = db["trends"]

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get("http://x.com/i/flow/login")

try:
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
    )
    sleep(1)
    email_field.send_keys(app.config['email'])

    next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
    next_button.click()

    username_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
    )
    sleep(1)
    username_field.send_keys("ayushsingh53718")
    
    next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
    next_button.click()

    password = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
    )
    sleep(1)
    password.send_keys(app.config['password'])
    login = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
    login.click()

except Exception as e:
    print(f"An error occurred during login: {e}")
    driver.save_screenshot('error_screenshot.png')

try:
    trends = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@data-testid, 'trend')]"))
    )
    trending_topics = [trend.text for trend in trends[:5]]
    print(trending_topics)

    ip_address = generate_random_ip()
    print(f"The IP address used for this query was {ip_address}.")

    unique_id = str(uuid.uuid4())
    timestamp = datetime.now()

    record = {
        "_id": unique_id,
        "trend1": trending_topics[0] if len(trending_topics) > 0 else "",
        "trend2": trending_topics[1] if len(trending_topics) > 1 else "",
        "trend3": trending_topics[2] if len(trending_topics) > 2 else "",
        "trend4": trending_topics[3] if len(trending_topics) > 3 else "",
        "trend5": trending_topics[4] if len(trending_topics) > 4 else "",
        "timestamp": timestamp,
        "ip_address": ip_address,
    }

    collection.insert_one(record)
    print("Trends saved to MongoDB")

except Exception as e:
    print(f"An error occurred during scraping: {e}")

driver.quit()
