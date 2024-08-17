# Sugar Price Data Scraper and Converter

This Python script automates the process of scraping historical sugar price data from Investing.com, converting it to INR, and saving it to an Excel file.

## Features

* Scrapes weekly historical data from the given URL.
* Extracts relevant data points: Date, Price, Change %.
* Converts price to INR using an external exchange rate API.
* Creates a pandas DataFrame with additional columns: Product Name, Day.
* Saves the DataFrame to an Excel file named "Output.xlsx".

## Requirements

* Python 3.x
* Selenium (for web scraping)
* pandas (for data manipulation)
* openpyxl (for Excel file creation)
* requests (for making API calls)

## Instructions

1. **Install Dependencies:**

   ```bash
   pip install selenium pandas openpyxl requests