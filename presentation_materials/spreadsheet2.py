import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import timeit
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import basic_test
import advanced_tests

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.


# change to:
sheet0 = client.open("Selenium Tests")
sheet = sheet0.get_worksheet(0)

results = client.open("Selenium Tests").get_worksheet(1)


#results.clear()

# Extract and print all of the values
list_of_sites = sheet.get_all_values()

i = 1

for site in list_of_sites:
    if site[0] != 'URL':

        # Create a new instance of the Firefox driver
        # modify: add the geckodriver's location to my path so python knows where to search for it    
        # driver = webdriver.Firefox(executable_path = '/Users/sherrili/Desktop/geckodriver')
        driver = webdriver.Firefox()

        basic_result = basic_test.basic_test(driver, results, site[0], i)
        
        
        # run advanced test if basic passed and advanced test requested
        if ((basic_result == 0) and (site[1] == 'y')):
            start_time = timeit.default_timer()
            advanced_result = advanced_tests.advanced_tests(driver, site[0], results, i)
            elapsed = timeit.default_timer() - start_time

            if advanced_result == 1:
                results.update_cell(i, 5, 'pass')
            else:
                results.update_cell(i, 5, 'fail')

            results.update_cell(i, 6, elapsed)

        elif site[1] == 'n':
            results.update_cell(i, 5, 'no advanced test')
        
        i=i+1
        driver.quit()

