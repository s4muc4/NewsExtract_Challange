from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import re
from typing import List

class LatimesExtractor:
    def __init__(self) -> None:
        """Initializing class of website"""
        self.browser = Selenium()
        self.table = Tables()

    def open_specific_browser(self):
        self.browser.open_browser(url="https://www.latimes.com/", browser="firefox")

    def close_browser(self):
        self.browser.close_browser()

    def search_by_phrase(self, phrase):
        self.browser.click_button("//button[@data-element='search-button']")
        self.browser.input_text("//input[@data-element='search-form-input']", phrase)
        self.browser.press_keys(None, "RETURN")
        try:
            self.browser.wait_until_element_is_enabled("//span[@class='search-results-module-count-desktop']","15")
            result = self.browser.get_text("//span[@class='search-results-module-count-desktop']")
            regex_numbers = re.findall(r'\d+', result)
            news_count = ''.join(regex_numbers)
            self.browser.wait_until_element_is_enabled("//select[@class='select-input']","30")
            self.browser.select_from_list_by_value("//select[@class='select-input']","1")
        except Exception as err:
            self.browser.wait_until_element_is_enabled("//div[@class='search-results-module-no-results']","30")
            news_count = self.browser.get_text("//div[@class='search-results-module-no-results']")
        finally:
            print(news_count)
        return int(news_count)
    
    def get_page_news(self):
        news:List[WebElement] = self.browser.get_webelements("//ul[@class='search-results-module-results-menu']/li/ps-promo") 
        
        for new in news:
            # Extract promo title
            title = new.find_element(By.CLASS_NAME, "promo-title").text
            date = new.find_element(By.CLASS_NAME, "promo-timestamp").text
            description = new.find_element(By.CLASS_NAME, "promo-description").text
            picture_link = new.find_element(By.CLASS_NAME, "image").get_attribute("srcset")
            picture_file_name = self.get_image_file_name(picture_link)
            href = new.find_element(By.TAG_NAME, "a").get_attribute("href")
            print("-----------------------------------------------------------------------------------------------------------------------")
            print("Title: "+title)
            print("Post Date: "+date)
            print("Description: "+description)
            print("Picture file name: "+picture_file_name)
            print("URL of new: "+href)
            print("-----------------------------------------------------------------------------------------------------------------------")

    def get_image_file_name(self, srcset):
        evidences = srcset.split('%')
        filename = "#"
        for evidence in evidences:
            if evidence.__contains__(".jpg") or evidence.__contains__(".jpeg") or evidence.__contains__(".png") or evidence.__contains__(".webp"):
                name = str(evidence).strip(" ")
                positions = name.split(" ")
                for position in positions:
                    if str(position).endswith(".jpg") or str(position).endswith(".jpeg") or str(position).endswith(".png") or str(position).endswith(".webp"):
                        filename = position
                        break
        if filename == "#":
            filename = "Filename not found because is without extension"
        return filename
        
        

    
    
    
        

    

    