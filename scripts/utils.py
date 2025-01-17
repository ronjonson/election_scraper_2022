from selenium import webdriver
from selenium.webdriver.common.by import By

import time


from dataclasses import dataclass, field


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