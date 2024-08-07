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
        news:List[WebElement] = self.browser.get_webelements("//*[@class='search-results-module-results-menu']") 


        for new in news:
            # Extract promo title
            title = new.find_element(
                    By.CLASS_NAME, "promo-title"
                ).text
            #title_element =  new.find_element() ('.//div[@class="promo-content"]/div[@class="promo-title-container"]/h3[@class="promo-title"]/a')
            #title = title_element.text
            print(title)

        
        

    
    
    
        

    

    