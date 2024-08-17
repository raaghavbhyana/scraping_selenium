import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import requests

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")

def setup_driver(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(10)

    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id=":R1b6:"]/form/div/button'))
        )
        close_button.click()
        print("Close Button Clicked")
    except TimeoutException:
        print("No close button found or unable to click it")
    time.sleep(2)

    time_frame_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[1]/div[2]'))
    )
    time_frame_element.click()
    weekly_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div[1]/div[2]/div/div[2]'))
    )
    weekly_option.click()
    time.sleep(5)

    return driver

def scrape_data_selenium_bs(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    table = soup.find('table', {'data-test': 'historical-data-table'})
    if not table:
        raise ValueError("Table not found on the page")
    
    table_data = []
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            date = cells[0].text.strip()
            price = cells[1].text.strip()
            table_data.append([date, price])
    
    return table_data

def create_dataframe(table_data):
    df = pd.DataFrame(table_data, columns=["Product Date", "Price"])
    df["Product Name"] = "Sugar"
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)
    return df

def add_day_column(df):
    df["Day"] = pd.to_datetime(df["Product Date"]).dt.day_name()
    return df

def convert_to_inr(df):
    url = 'https://v6.exchangerate-api.com/v6/86a8424b9225e7d5fda96501/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        inr_rate = data['rates']['INR']
        
        df["Price"] = df["Price"].str.replace(",", "").astype(float)
        df["Final Price (INR)"] = df["Price"] * inr_rate
    except Exception as e:
        print(f"Error converting to INR: {e}")
        df["Final Price (INR)"] = None
    return df

def save_to_excel(df, filename="Output.xlsx"):
    df.to_excel(filename, index=False, engine='openpyxl')

if __name__ == "__main__":
    url = "https://uk.investing.com/commodities/us-sugar-no11-historical-data"

    try:
        driver = setup_driver(url)
        table_data = scrape_data_selenium_bs(driver)
        driver.quit()

        df = create_dataframe(table_data)
        df = add_day_column(df)
        df = convert_to_inr(df)
        save_to_excel(df)
        print("Data extraction and conversion completed successfully!")
    except Exception as e:
        print("An error occurred:", e)