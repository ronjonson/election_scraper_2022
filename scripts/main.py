import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import fields

from constants import *
from classes import Location


class ElectionScraper:
    def __init__(self,
                region: str=None,
                province: str=None,
                city: str=None,
                brgy: str=None,
                precinct: str=None):
        
        # Value Error will be raised if lower tiered parameters have value if higher tier has value
        self.location = Location(region, province, city, brgy, precinct)
        ### initialize web driver
        self.driver = webdriver.Firefox()
        self.driver.get(SITE)

        self.start_location = self.location.get_start_location()

    def click_option(self, dropdown_xpath: str, list_xpath:str, driver:webdriver=None):
        """Selects the given dropdown and area (Region, Province, City, Barangay, Precinct)"""
        driver = self.driver if driver is None else driver

        driver.find_element(by=By.XPATH, value=dropdown_xpath).click()
        time.sleep(0.5)
        driver.find_element(by=By.XPATH, value=list_xpath).click()
        time.sleep(0.5)

    def get_dropdown_values(self, x_path:str, driver:webdriver) -> list:
        dropdown_list = driver.find_element(by=By.XPATH, value=x_path)
        values = dropdown_list.find_elements(by=By.TAG_NAME, value='li')

        return values

    def select_option(self, dropdown_xpath: str, list_xpath:str, choice,driver:webdriver=None):
        driver = self.driver if driver is None else driver
        self.click_option(dropdown_xpath, list_xpath, driver)
        options = self.get_dropdown_values(list_xpath, driver=driver)

        try:
            choice_index = options.index(choice)
            options[choice_index].click()

        except ValueError as e:
            raise ValueError(f'{choice} not found in list')
            

    def initialize_search(self):
        for key, value in self.start_location.items():
            self.select_option(DROPDOWN[key], DROPDOWN_VALUES[key], value)
            latest_key = key

        loc_fields = fields(self.location)

        if latest_key == 'precinct':
            pass
            #start search by searching this specific precinct
        elif latest_key in loc_fields:
            index = loc_fields.index(latest_key)
            
            #start search by going thru loc_fields[index+1]

        # iterate thru all left
        # save data somewhere
if last_key in fields:
    index = fields.index(last_key)
    # Check if there's a next item after the last_key
    if index + 1 < len(fields):
        next_value = fields[index + 1]
    else:
        next_value = None  # No next value (last_key is the last element)
else:
    next_value = None  # last_key is not in the fields list

if __name__ == '__main__':
    pass