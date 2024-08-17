from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time



driver=webdriver.Chrome()
driver.get("https://uk.investing.com/commodities/us-sugar-no11-historical-data")
time.sleep(8)


try:
    close_button=WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id=":R1b6:"]/form/div/button')))
        # Your expected condition here
    close_button.click()
except TimeoutException:
    print("The close button was not found within the specified time.")
    # Add any necessary error handling or recovery code here

