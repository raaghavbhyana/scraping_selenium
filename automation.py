import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
from selenium.common.exceptions import TimeoutException
import openpyxl

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")

def scrape_data(url):
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
    table_data= WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.freeze-column-w-1.w-full.overflow-x-auto.text-xs.leading-4"))
    )
    
    # Allow some time for dynamic content to load
    time.sleep(5)
    rows = table_data.find_elements(By.XPATH, ".//tbody/tr[contains(@class, 'historical-data-v2_price')]")
    print(rows)
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 7:
            date = cells[0].text
            price = cells[1].text
            change_percent = cells[6].text
            data.append({"Date": date, "Price": price, "Change %": change_percent})

    print(data)
    return data



def create_dataframe(data):
    df = pd.DataFrame(data)
    df["Product Name"] = "Sugar"  # Assuming all data is for sugar

    # Handle duplicates and NaN values
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)
    print(df)

    return df

def add_day_column(df):
    try:
        df["Date"] = pd.to_datetime(df["Date"], format="%b %d, %Y")
        df["Day"] = df["Date"].dt.day_name()
    except ValueError as e:
        print(f"Error converting date: {e}")
        # Handle the error (e.g., replace with NaN, remove row, etc.)
    return df

def convert_to_inr(df):
    # url = 'https://v6.exchangerate-api.com/v6/86a8424b9225e7d5fda96501/latest/USD'
    try:
        url = 'https://v6.exchangerate-api.com/v6/86a8424b9225e7d5fda96501/latest/USD'
        response = requests.get(url)
        data = response.json()
        inr_rate = data['conversion_rates']['INR']
        
        df['Price'] = df['Price'].astype(float)
        
        df["Final Price (INR)"] = df["Price"] * inr_rate
    except Exception as e:
        print(f"Error converting to INR: {e}")
        df["Final Price (INR)"] = None
    return df

def save_to_excel(df, filename="Output.xlsx"):
    df.to_excel(filename, index=False, engine='openpyxl')

if __name__ == "__main__":
    url = "https://uk.investing.com/commodities/us-sugar-no11-historical-data"
    # api_key = "YOUR_API_KEY"  # Replace with your API key

    try:
        table_data = scrape_data(url)
        df = create_dataframe(table_data)
        df = add_day_column(df)
        df = convert_to_inr(df)
        save_to_excel(df)
        print("Data extraction and conversion completed successfully!")
    except Exception as e:
        print("An error occurred:", e)
        # Handle the error appropriately (e.g., log, retry, notify)