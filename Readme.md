# Sugar Price Data Scraper and Converter

This Python script automates the process of scraping historical sugar price data from Investing.com, converting it to INR, and saving it to an Excel file.

## Features

* Scrapes weekly historical data from the given URL.
* Extracts relevant data points: Date, Price, Change %.
* Converts price to INR using an external exchange rate API.
* Creates a pandas DataFrame with additional columns: Product Name, Day.
* Saves the DataFrame to an Excel file named "Output.xlsx".
## Project Components

1. **automation.py**: 
   - This script contains the code to scrape data from the website [Investing.com](https://uk.investing.com/commodities/us-sugar-no11-historical-data) using Selenium, process the data using Pandas, and perform data manipulation tasks.
   
2. **Output.xlsx**: 
   - This Excel file contains the final output of the data after manipulation, including converted prices and additional columns created during processing.

## Requirements

* Python 3.x
* Selenium (for web scraping)
* pandas (for data manipulation)
* openpyxl (for Excel file creation)
* requests (for making API calls)

## Instructions

1. **Clone the repository:**

   ```bash
   gh repo clone raaghavbhyana/scraping_selenium
2. **Install Dependencies:**

   ```bash
   pip install selenium pandas openpyxl requests

   or 

   pip install -r requirements.txt

### Execution

1. **Run the Script:**
Execute the `automation.py` script to start the web scraping and data analysis process:
2. **Data Processing:**
The script will perform the following tasks:
- Navigate to the specified URL and set the "Time Frame" to "Weekly."
- Scrape the product price table (Price, Product Date).
- Handle duplicate or NaN values in the data.
- Add a "Day" column to determine the day of the week for each Product Date.
- Convert the prices from USD to INR using an open-source API and store them in the "Final Price (INR)" column. (Using ExchangeRate-API) https://www.exchangerate-api.com free api
- Export the processed data to `Output.xlsx`.

3. **Output:**
The final processed data will be saved in an Excel file named `Output.xlsx`, structured with the required columns.




 


