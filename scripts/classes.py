from dataclasses import dataclass, field, fields, astuple

import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    def is_complete(self) -> bool:
        if self.PRECINCT is not None:
            return True
        else:
            return False


    def save_current_location(self):
        pass


class ElectionScraper:
    def __init__(self,
                region: str=None,
                province: str=None,
                city: str=None,
                barangay: str=None,
                precinct: str=None,
                save_filepath: str='data.csv',
                max_attempts: int=5):
        region = region.upper() if region is not None else region
        province = province.upper() if province is not None else province
        city = city.upper() if city is not None else city
        barangay = barangay.upper() if barangay is not None else barangay
        precinct = precinct.upper() if precinct is not None else precinct

        # Value Error will be raised if lower tiered parameters have value if higher tier has value
        self.location = Location(region, province, city, barangay, precinct)

        #initialize current location to track history
        self.cur_location = Location(
            REGION=self.location.REGION,
            PROVINCE=self.location.PROVINCE,
            CITY=self.location.CITY,
            BARANGAY=self.location.BARANGAY,
            PRECINCT=self.location.PRECINCT
        )
        
        self.history = set()

        self.start_location = self.location.get_start_location()
        
        self.max_attempts = max_attempts

        self.save_filepath = save_filepath

    def click_option(self, dropdown_xpath: str, driver:webdriver=None):
        """Selects the given dropdown and area (Region, Province, City, Barangay, Precinct)"""
        driver = self.driver if driver is None else driver
        option = WebDriverWait(driver, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, dropdown_xpath))
        )
        option.click()
        #driver.find_element(by=By.XPATH, value=dropdown_xpath).click()

    def get_dropdown_values(self, x_path:str, driver:webdriver=None) -> list:
        if driver is None:
            driver = self.driver

        dropdown_list = driver.find_element(by=By.XPATH, value=x_path)
        values = dropdown_list.find_elements(by=By.TAG_NAME, value='li')

        return values

    def select_option(self, dropdown_xpath: str, list_xpath:str, choice:str, driver:webdriver=None):
        driver = self.driver if driver is None else driver
        self.click_option(dropdown_xpath, driver)
        options = self.get_dropdown_values(list_xpath, driver=driver)

        for option in options:
            #print(f"option.text: {option.text}")
            if option.text == choice:
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(option))
                option.click()
                return

        raise ValueError(f'{choice} not found in list. Please choose the following options: {", ".join(options)}')
            
    def clear_textbox(self, textbox_xpath:str, value:str=None,driver:webdriver=None):
        driver = self.driver if driver is None else driver
        textbox = driver.find_element(By.XPATH, f"//input[@value='{value}']")
        textbox.clear()

    def update_current_location(self, level:str, value:str):
        setattr(self.cur_location, level, value)
        # Reset lower hierarchy fields
        all_fields = [f.name for f in fields(self.location)]
        current_index = all_fields.index(level)
        for lower_field in all_fields[current_index + 1:]:
            setattr(self.cur_location, lower_field, None)
    
    def _get_location_tuple_(self):
        return (
            self.cur_location.REGION,
            self.cur_location.PROVINCE,
            self.cur_location.CITY,
            self.cur_location.BARANGAY,
            self.cur_location.PRECINCT
        )
    def _parse_local_results_(self, text):
        results = []
        clean_text = text.partition(
        "Statistical Information"
        )[0].strip()

        lines = [
            line.strip()
            for line in clean_text.split("\n")
            if line.strip()
        ]

        # first line is the position
        position = lines[0]

        start_idx = lines.index("Candidate")

        candidate_lines = lines[start_idx + 3:]

        for i in range(0, len(candidate_lines), 3):

            if i + 2 >= len(candidate_lines):
                break

            data_row = [
                position,
                candidate_lines[i],       # candidate
                candidate_lines[i + 1],   # votes
                candidate_lines[i + 2],   # percentage
            ]

            results.append(data_row)

        return results

    def scrape_table_info(self, driver:webdriver=None) -> list:
        driver = self.driver if driver is None else driver
        headers = ['region','province','city','barangay','precinct','position', 'candidate', 'votes', 'percentage']
        data = [headers]

        # Wait until the table is present before scraping data
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,DATA_TABLES['PRESIDENT']))
        )

        for position, table_xpath in DATA_TABLES.items():
            #table = driver.find_element(By.XPATH, table_xpath)
            tmp_data = []
            for attempt in range(self.max_attempts):
                try:
                    rows = driver.find_elements(By.XPATH, f"{table_xpath}/div")
                    row_texts = [row.text for row in rows]
                    for row in row_texts:
                        data_row = [self.cur_location.REGION,
                                self.cur_location.PROVINCE,
                                self.cur_location.CITY,
                                self.cur_location.BARANGAY,
                                self.cur_location.PRECINCT,
                                position]
                        data_row.extend(row.split("\n"))
                        tmp_data.append(data_row)

                    break
                except Exception as e:
                    print(f"Error occurred while scraping table info: {e}")
                    if attempt < self.max_attempts - 1:
                        print("Retrying...")
                    
            data.extend(tmp_data)

        local_results_element = self.driver.find_element(
            By.XPATH,
            "//*[@ng-if='showLocal']"
        )
        local_results_children = local_results_element.find_elements(By.XPATH, "./*")
        for res in local_results_children[1:]:
            data.extend(self._parse_local_results_(res.text))

        return data
    
    def _save_data(self, data: list):
        if self.save_filepath is None:
            raise ValueError("save_filepath must be specified to save data.")
        
        with open(self.save_filepath, 'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def scrape_data(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)
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
            print(f" Current Location is :{self.cur_location}")
            if current_level == 'PRECINCT':
                if self.location.is_complete():
                    self.update_current_location(current_level, self.location.PRECINCT)
                # Start scraping data at the precinct level
                #self.scrape_precinct_data()

                print("Scraping precinct data!")

                #metadata = self.driver.find_element(by=By.TAG_NAME, value="results-viewer")
                #print(metadata)
                data = self.scrape_table_info()
                print("Data scraped")
                self._save_data(data)
                print("saving Data")

            else:
                # Get the next level in the hierarchy
                for i , field in enumerate(loc_fields):
                    if field.name == current_level:
                        next_level_index = i+1
                        break

                if next_level_index < len(loc_fields):
                    print(f"Getting next level: {loc_fields[next_level_index].name}")
                    next_level = loc_fields[next_level_index].name

                    placeholder_value = f"//input[@placeholder='{DROPDOWN_PLACEHOLDER[next_level]}']"
                    options = []

                    while len(options) == 0:
                        try:
                            print("Trying to click option using placeholder...")
                            self.click_option(placeholder_value, driver=self.driver)
                        except:
                            print("Failed to click option using placeholder. Trying to click option using dropdown...")
                            self.click_option(DROPDOWN[next_level], self.driver)
                        
                        time.sleep(0.1)
                        options = self.get_dropdown_values(DROPDOWN_VALUES[next_level], driver=self.driver)
                        option_texts = [option.text for option in options]

                        print(f"options for {next_level}: {option_texts}")
                    
                    for option in option_texts:
                        #loc_text = option.text
                        precinct_loc = self._get_location_tuple_()[:-1] + (option,)
                        
                        if precinct_loc in self.history:
                            # skip if current config of locations have already been visited
                            continue

                        self.select_option(
                            DROPDOWN[next_level],
                            DROPDOWN_VALUES[next_level],
                            option,
                            self.driver
                        )
                        
                        # Update current location to the next level with the option text
                        self.update_current_location(
                            next_level,
                            option
                        )

                        # Save current config to history so that we dont visit same lcoation 
                        self.history.add(
                            self._get_location_tuple_()
                        )

                        print(self.cur_location)

                        scrape_level(next_level)

                        self.update_current_location(
                            next_level,
                            None
                        )

                        #self.update_current_location(next_level, None)
                        # Reset to the current level after scraping the next level
                        # to reset, find element with same value of option.text and click
                        self.click_option(DROPDOWN[next_level], driver=self.driver)
                        
                        print("Getting textbox")
                        print(f"next_level: {next_level}")

                        textbox = self.driver.find_element(
                            By.XPATH,
                            f"//input[@placeholder='{DROPDOWN_PLACEHOLDER[next_level]}']"
                        )
                        
                        # Clear the textbox
                        try:
                            textbox.clear()
                        
                        except:
                            textbox.send_keys(Keys.CONTROL + "a")
                            textbox.send_keys(Keys.DELETE)

        for key, value in self.start_location.items():
            print(f"Scraping {key} data!")
            print(f"value: {value}")
            
            for i in range(self.max_attempts):
                try:
                    print("Trying to select option using placeholder...")
                    self.select_option(f"//input[@placeholder='{DROPDOWN_PLACEHOLDER[key]}']", DROPDOWN_VALUES[key], value, self.driver)
                    break
                except:
                    try:
                        print("Failed to select option using placeholder. Trying to select option using dropdown...")
                        self.select_option(DROPDOWN[key], DROPDOWN_VALUES[key], value, self.driver)
                        break
                    except:
                        print("Failed to select option using dropdown. Retrying...")
                        
                        if i < self.max_attempts - 1:
                            continue
                        else:
                            raise Exception(f"Failed to select option after {self.max_attempts} attempts. Please check if the option exists and if the xpaths are correct.")

            latest_key = key

        loc_fields = fields(self.location)

        scrape_level(latest_key)