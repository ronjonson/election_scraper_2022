from dataclasses import dataclass, field, fields

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import fields

from constants import *

@dataclass
class Location:
    country: str = field(default='PHILIPPINES')
    region: str = field(default=None)
    province: str = field(default=None)
    city: str = field(default=None)
    barangay: str = field(default=None)
    precinct: str = field(default=None)

    def __post_init__(self):
        # Retrieve the fields in the class in their defined order
        all_fields = [f.name for f in fields(self) if f.name != "country"]
        for i, field_name in enumerate(all_fields):
            field_value = getattr(self, field_name)
            # Ensure no lower hierarchy field is set if a higher one is None
            if field_value is None:
                for lower_field in all_fields[i+1:]:
                    if getattr(self, lower_field) is not None:
                        raise ValueError(
                            f"{field_name.capitalize()} must be specified before {lower_field.capitalize()}."
                        )

    def __setattr__(self, name, value):
        all_fields = [f.name for f in fields(self)]
        if name in all_fields:
            # Set the value for the current field
            super().__setattr__(name, value)
            # Reset lower hierarchy fields
            current_index = all_fields.index(name)
            for lower_field in all_fields[current_index + 1:]:
                super().__setattr__(lower_field, None)
        else:
            super().__setattr__(name, value)

    def get_start_location(self) -> dict:
        location = {}
        for field in fields(self):
            field_name = field.name
            field_value = getattr(self, field_name)
            if field_value is None:
                return location
            location[field_name] = field_value
        return location
    
    def save_current_location(self):
        pass


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
            raise ValueError(f'{choice} not found in list. Please choose the following options: {', '.join(options)}')
            

    def initialize_search(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE)
        
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

        """if last_key in fields:
            index = fields.index(last_key)
            # Check if there's a next item after the last_key
            if index + 1 < len(fields):
                next_value = fields[index + 1]
            else:
                next_value = None  # No next value (last_key is the last element)
        else:
            next_value = None  # last_key is not in the fields list"""