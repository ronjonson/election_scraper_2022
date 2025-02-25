from dataclasses import dataclass, field, fields

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import fields

from constants import *

@dataclass
class Location:
    REGION: str = field(default=None)
    PROVINCE: str = field(default=None)
    CITY: str = field(default=None)
    BARANGAY: str = field(default=None)
    PRECINCT: str = field(default=None)

    def __post_init__(self):
        # Retrieve the fields in the class in their defined order
        all_fields = [f.name for f in fields(self)]
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
                barangay: str=None,
                precinct: str=None):
        region = region.upper() if region is not None else region
        province = province.upper() if province is not None else province
        city = city.upper() if city is not None else city
        barangay = barangay.upper() if barangay is not None else barangay
        precinct = precinct.upper() if precinct is not None else precinct

        # Value Error will be raised if lower tiered parameters have value if higher tier has value
        self.location = Location(region, province, city, barangay, precinct)
        ### initialize web driver


        self.start_location = self.location.get_start_location()
        

    def click_option(self, dropdown_xpath: str, driver:webdriver=None):
        """Selects the given dropdown and area (Region, Province, City, Barangay, Precinct)"""
        driver = self.driver if driver is None else driver
        time.sleep(0.25)
        driver.find_element(by=By.XPATH, value=dropdown_xpath).click()
        time.sleep(0.25)

    def get_dropdown_values(self, x_path:str, driver:webdriver) -> list:
        dropdown_list = driver.find_element(by=By.XPATH, value=x_path)
        values = dropdown_list.find_elements(by=By.TAG_NAME, value='li')

        return values

    def select_option(self, dropdown_xpath: str, list_xpath:str, choice:str, driver:webdriver=None):
        driver = self.driver if driver is None else driver
        self.click_option(dropdown_xpath, driver)
        options = self.get_dropdown_values(list_xpath, driver=driver)

        for option in options:
            print(f"option.text: {option.text}")
            if option.text == choice:
                option.click()
                return

        raise ValueError(f'{choice} not found in list. Please choose the following options: {', '.join(options)}')
            
    def clear_textbox(self, textbox_xpath:str, value:str=None,driver:webdriver=None):
        driver = self.driver if driver is None else driver
        textbox = driver.find_element(By.XPATH, f"//input[@value='{value}']")
        textbox.clear()
        
    def scrape_data(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE)

        # hierarchy of data is Country -> Region -> Province -> City -> Barangay -> Precinct
        # 1. Go through hierarchy of data based on self.start_location to get to the precinct level/lowest level that is not None(can be not precinct)
        #   1.a. to get to page of lowest location, use self.select_option(dropdown_xpath,list_xpath,choice) to select the location.
        #   1.b. the dropdown_xpath is taken from a dictionary of DROPDOWN in constants.py, the list_xpath is taken from a dictionary of DROPDOWN_VALUES in constants.py
        # 2. Once at lowest level
        #   2.a. if at location is at precinct, start scraping data
        #   2.b. if not, iterate through all locations and get all possible data
        #       2.b.i. ex. if at city level, iterate through all barangays and all precinct within each barangay and get all possible data
        #   2.c. save data somewhere 

        def scrape_level(current_level):
            if current_level == 'PRECINCT':
                # Start scraping data at the precinct level
                #self.scrape_precinct_data()
                print("Scraping precinct data! brrbrr")
                
            else:
                # Get the next level in the hierarchy
                for i , field in enumerate(loc_fields):
                    if field.name == current_level:
                        next_level_index = i+1
                        break

                if next_level_index < len(loc_fields):
                    next_level = loc_fields[next_level_index].name

                    placeholder_value = f"//input[@placeholder='{DROPDOWN_PLACEHOLDER[next_level]}']"
                    try:
                        self.click_option(placeholder_value, driver=self.driver)
                    except:
                        self.click_option(DROPDOWN[key], DROPDOWN_VALUES[key], value, self.driver)
                    options = self.get_dropdown_values(DROPDOWN_VALUES[next_level], driver=self.driver)
                    for option in options:
                        current_text = option.text
                        option.click()
                        scrape_level(next_level)
                        # Reset to the current level after scraping the next level
                        # to reset, find element with same value of option.text and click
                        self.click_option(DROPDOWN[next_level], driver=self.driver)
                        self.driver.find_element(by=By.XPATH, value=placeholder_value).clear()
                        
                        # Clear the textbox
                        textbox_xpath = DROPDOWN[next_level].replace('dropdown', 'textbox')
                        textbox = self.driver.find_element(by=By.XPATH, value=textbox_xpath)
                        textbox.clear()


    

        for key, value in self.start_location.items():
            print(f"Scraping {key} data!")
            print(f"value: {value}")
            try:
                self.select_option(f"//input[@placeholder='{DROPDOWN_PLACEHOLDER[key]}']", DROPDOWN_VALUES[key], value, self.driver)
            except:
                self.select_option(DROPDOWN[key], DROPDOWN_VALUES[key], value, self.driver)

            latest_key = key

        loc_fields = fields(self.location)


        scrape_level(latest_key)