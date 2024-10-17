from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://www.sick.com/in/en/catalog/products/detection-sensors/photoelectric-sensors/w4/wtb4fp-22161120a00/p/p661408?tab=detail")

time.sleep(3)
try:
    accept_button = driver.find_element(By.ID, 'gdpr_modal_button_consent')
    accept_button.click()
    print("Accepted cookies.")
    time.sleep(5)
except Exception as e:
    print("No cookie popup found:", e)

soup = BeautifulSoup(driver.page_source, 'html.parser')
tech_table_div = soup.find('div', class_='tech-table')
table = tech_table_div.find('table')

table_rows = table.find_all('tr')
data = []
for row in table_rows:
    cols = row.find_all(['td', 'th'])
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

df = pd.DataFrame(data)
print(df)

try:
    img_tag = soup.find('img', class_='block margin-auto loaded')
    if img_tag and 'data-src' in img_tag.attrs:
        img_url = img_tag['data-src']
        print(f"Downloading image from: {img_url}")
        
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            with open("IM0085707.png", "wb") as file:
                file.write(img_response.content)
            print("Image downloaded successfully!")
        else:
            print("Failed to download image. Status code:", img_response.status_code)
    else:
        print("No image found with the specified class.")
except Exception as e:
    print("Error while downloading image:", e)

try:
    english_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.action-button.flex-grow.font-bold'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", english_button)
    driver.execute_script("arguments[0].click();", english_button)
    print("Clicked the English button successfully!")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tech-table')))
    print("New content loaded successfully!")
    time.sleep(20)
except Exception as e:
    print("Error while clicking the download button:", e)

driver.quit()
