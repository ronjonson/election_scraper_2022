from selenium import webdriver
from selenium.webdriver.common.by import By

import time


from dataclasses import dataclass, field

@dataclass
class Location:
    country: str = field(default=None)
    region: str = field(default=None)
    province: str = field(default=None)
    city: str = field(default=None)
    barangay: str = field(default=None)
    precinct: str = field(default=None)

    def set_country(self, value: str=None):
        self.country = value
        # Reset lower hierarchy
        self.set_region()

    def set_region(self, value: str=None):
        self.region = value
        # Reset lower hierarchy
        self.set_province()

    def set_province(self, value: str=None):
        self.province = value
        # Reset lower hierarchy
        self.set_city()

    def set_city(self, value: str=None):
        self.city = value
        # Reset lower hierarchy
        self.set_barangay()

    def set_barangay(self, value: str=None):
        self.barangay = value
        # Reset lower hierarchy
        self.set_precinct()

    def set_precinct(self, value: str=None):
        self.precinct = value


    def __setattr__(self, name, value):
        if name == "country":
            self.set_country(value)
        elif name == "region":
            self.set_region(value)
        elif name == "province":
            self.set_province(value)
        elif name == "city":
            self.set_city(value)
        elif name == "barangay":
            self.set_barangay(value)
        elif name == "precinct":
            self.set_precinct(value)
        else:
            super().__setattr__(name, value)

    def save_current_location(self):
        pass


def click_option(driver:webdriver, dropdown_xpath: str, list_xpath:str):
    """Selects the given dropdown and area (Region, Province, City, Barangay, Precinct)"""
    driver.find_element(by=By.XPATH, value=dropdown_xpath).click()
    time.sleep(0.5)
    driver.find_element(by=By.XPATH, value=list_xpath).click()
    time.sleep(0.5)

def get_dropdown_values(driver:webdriver, x_path:str):
    dropdown_list = driver.find_element(by=By.XPATH, value=x_path)
    values = dropdown_list.find_elements(by=By.TAG_NAME, value='li')

    return values

def clear_textbox(driver:webdriver, loc_arrow_xpath:str, textbox:str):
    driver.find_element(By.XPATH,loc_arrow_xpath).click()
    time.sleep(0.125)
    driver.find_element(By.XPATH,textbox).clear()