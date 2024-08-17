from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
from datetime import datetime
import requests

# Configure and initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to the website and set the time frame
url = 'https://uk.investing.com/commodities/us-sugar-no11-historical-data'
driver.get(url)
close_button=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id=":rb:"]/form/div/button')))
close_button.click()
# Wait for the time frame dropdown to be clickable
time_frame = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'data_interval'))
)
Select(time_frame).select_by('Weekly')

# Wait for the page to load after changing the time frame
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'curr_table'))
)

# Extract the table data
table = driver.find_element(By.ID, 'curr_table')
rows = table.find_elements(By.TAG_NAME, 'tr')

data = []
for row in rows[1:]:  # Skip the header row
    cols = row.find_elements(By.TAG_NAME, 'td')
    if len(cols) > 0:
        date = cols[0].text
        price = cols[1].text
        data.append({'Product Date': date, 'Price': price})


df = pd.DataFrame(data)
df['Product Name'] = 'Sugar'  # Add the product name column

# Process and clean the data
df['Price'] = df['Price'].str.replace(',', '').astype(float)
df['Product Date'] = pd.to_datetime(df['Product Date'])
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Add the "Day" column
df['Day'] = df['Product Date'].dt.day_name()

# Convert USD to INR
def usd_to_inr(usd_amount):
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    inr_rate = data['rates']['INR']
    return usd_amount * inr_rate

df['Final Price (INR)'] = df['Price'].apply(usd_to_inr)

# Write the output to an Excel file
df = df[['Product Name', 'Price', 'Product Date', 'Day', 'Final Price (INR)']]
df.to_excel('Output.xlsx', index=False)