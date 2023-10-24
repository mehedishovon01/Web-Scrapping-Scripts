import os
import time
import logging
import pygsheets
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Constants
COUNTRIES = {
    "Indonesia": "https://www.investing.com/equities/indonesia",
    "USA": "https://www.investing.com/equities/united-states",
    "Hongkong": "https://www.investing.com/equities/hong-kong",
    "Germany": "https://www.investing.com/equities/germany",
    "UK": "https://www.investing.com/equities/united-kingdom",
    "Canada": "https://www.investing.com/equities/canada",
    "Japan": "https://www.investing.com/equities/japan",
    "China": "https://www.investing.com/equities/china",
    "France": "https://www.investing.com/equities/france",
    "South Korea": "https://www.investing.com/equities/south-korea",
    "Taiwan": "https://www.investing.com/equities/taiwan",
    "Australia": "https://www.investing.com/equities/australia",
    "Netherlands": "https://www.investing.com/equities/netherlands",
    "Singapore": "https://www.investing.com/equities/singapore",
    "Thailand": "https://www.investing.com/equities/thailand",
    "Malaysia": "https://www.investing.com/equities/malaysia",
    "Belgium": "https://www.investing.com/equities/belgium",
    "Philippines": "https://www.investing.com/equities/philippines",
    "Turkey": "https://www.investing.com/equities/turkey",
    "Vietnam": "https://www.investing.com/equities/vietnam",
    "Portugal": "https://www.investing.com/equities/portugal"
    # Add more countries here
}

load_dotenv()
GOOGLE_SHEET_CREDENTIALS = os.getenv('GOOGLE_SHEET_CREDENTIALS')
GOOGLE_SHEET_NAME = 'Scrapping testing'

def scrape_stock_data(driver, wait, url):
    """
    The function takes the URL of a country's stock performance page as an input. It uses a Selenium WebDriver to open the provided URL.
    It waits for the page to fully load by employing the WebDriverWait mechanism with a specified timeout (WAIT_TIMEOUT_SECONDS).
    Finds and clicks on the tab with the attribute data-test-tab-id="1". The extracted data is stored as a list of dictionaries.
    :param driver:
    :param wait: WebDriverWait
    :param url: country url
    :return: list of extracted data
    """
        
    # Navigate to the URL
    newURL = f"{url}/top-stock-gainers"
    driver.get(newURL)
    wait.until(EC.url_to_be(newURL))

    page_source = driver.page_source
    BeautifulSoup(page_source, features="html.parser")

    # Find and click the tab with data-test-tab-id="1"
    tab = driver.find_element(By.CSS_SELECTOR, '[data-test-tab-id="1"]')
    tab.click()

    # Allow some time for the hidden table to load
    time.sleep(5)

    # Find the revealed table and scrape its data
    tab_data = driver.find_element(By.CSS_SELECTOR, '[class="datatable_body__tb4jX"]')
    performance_data = tab_data.find_elements(By.TAG_NAME, 'tr')

    country_performance = []
    for row in performance_data:
        columns = row.find_elements(By.TAG_NAME, 'td')
        name = columns[0].text.strip()
        monthly = columns[3].text.strip()

        stock_info = {
            "Name": name,
            "Month": monthly
        }
        country_performance.append(stock_info)

    return country_performance


def main():
    """
    This function uses to authenticate with Google Sheets & WebDriver Initialization using the specified credentials file
    Also Selenium web scraping using the ChromeDriverManager. It calls the scrape_stock_data function to scrape stock performance. 
    Also this function performs to Navigates URL, Waits for the page to load fully, Clicks on the tab with data-test-tab-id="1" 
    to reveal the performance table, extracts data from the table, including stock names and monthly performance.
    :return: None
    """
    try:
        # Initialize the Selenium Chrome driver with the specified options
        driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        wait = WebDriverWait(driver, 10)

        # Authorization google spreadsheet credentials
        credentials = pygsheets.authorize(service_file=GOOGLE_SHEET_CREDENTIALS)

        for country, url in COUNTRIES.items():
            try:
                country_performance = scrape_stock_data(driver, wait, url)

                # Convert the list of dictionaries to a pandas DataFrame
                df = pd.DataFrame(country_performance)

                # Sort the DataFrame by the 'Month' column in ascending order
                df['Month'] = df['Month'].str.rstrip('%').astype(float)
                sorted_df = df.sort_values(by='Month', ascending=False)
                sorted_df['Month'] = sorted_df['Month'].astype(str) + '%'
                
                # Open the google spreadsheet (where 'GOOGLE_SHEET_NAME' is the name of my sheet)
                spreadsheet = credentials.open(GOOGLE_SHEET_NAME)

                # Check if a worksheet with the same name already exists
                worksheet_name = country
                while worksheet_name in [worksheet.title for worksheet in spreadsheet.worksheets()]:
                    worksheet_name += "(1)"

                # Add a new worksheet for the country
                worksheet = spreadsheet.add_worksheet(worksheet_name)

                # Print the data to the Google Sheet starting from cell A1
                worksheet.set_dataframe(sorted_df, start='A1')

            except Exception as error:
                logging.error(f"Error while scraping {country}: {error}")

        # Quit the Selenium driver
        driver.quit()

    except Exception as error:
        logging.error(f"Exception while Authorization: {error}")

if __name__ == "__main__":
    start = time.time()
    main()
    # Print the executable time need this script
    print(f'This script took {round(time.time() - start, 2)} seconds to generate the results')
