from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import re
from typing import List

class LatimesExtractor:
    def __init__(self,count_news: int, phrase, sort_by, date) -> None:
        """Initializing class of website"""
        self.browser = Selenium()
        self.table = Tables()
        self.count_news = count_news
        self.date = date
        self.phrase = phrase
        self.sort_by = sort_by
    def open_specific_browser(self):
        self.browser.open_browser(url="https://www.latimes.com/", browser="firefox")

    def close_browser(self):
        self.browser.close_browser()

    def search_by_phrase(self):
        self.browser.click_button("//button[@data-element='search-button']")
        self.browser.input_text("//input[@data-element='search-form-input']", self.phrase)
        self.browser.press_keys(None, "RETURN")
        try:
            self.browser.wait_until_element_is_enabled("//span[@class='search-results-module-count-desktop']","15")
            result = self.browser.get_text("//span[@class='search-results-module-count-desktop']")
            regex_numbers = re.findall(r'\d+', result)
            news_count = ''.join(regex_numbers)
            self.browser.wait_until_element_is_enabled("//select[@class='select-input']","30")
            try:
                self.browser.select_from_list_by_label("//select[@class='select-input']",self.sort_by)
            except Exception as err:
                self.browser.select_from_list_by_label("//select[@class='select-input']","Relevance")
                
        except Exception as err:
            self.browser.wait_until_element_is_enabled("//div[@class='search-results-module-no-results']","30")
            news_count = self.browser.get_text("//div[@class='search-results-module-no-results']")
        finally:
            print(str(news_count) +" results found." )
        return int(news_count)
    
    def get_page_news(self):
        count_news_found = 0
        finished = False
        while finished == False or count_news_found < self.count_news:
            news:List[WebElement] = self.browser.get_webelements("//ul[@class='search-results-module-results-menu']/li/ps-promo") 
            for new in news:
                if count_news_found < self.count_news: 
                    title = new.find_element(By.CLASS_NAME, "promo-title").text
                    try:
                        topic = new.find_element(By.XPATH, "//p[@class='promo-category']/a").text
                        date = new.find_element(By.CLASS_NAME, "promo-timestamp").text
                        description = new.find_element(By.CLASS_NAME, "promo-description").text
                        picture_link = new.find_element(By.CLASS_NAME, "image").get_attribute("srcset")
                        picture_file_name = self.get_image_file_name(picture_link)
                        href = new.find_element(By.TAG_NAME, "a").get_attribute("href")
                        count_news_found += 1
                        print("-----------------------------------------------------------------------------------------------------------------------")
                        print("New number: " + str(count_news_found))
                        print("Title: "+title)
                        print("Topic: "+topic)
                        print("Post Date: "+date)
                        print("Description: "+description)
                        print("Picture file name: "+picture_file_name)
                        print("URL of new: "+href)
                        print("-----------------------------------------------------------------------------------------------------------------------")
                        """Send data to excel file"""
                    except Exception as err:
                        print("Error to get new from " + title)
                else:
                    finished = True
            if finished == False:
                try:
                    self.browser.click_element_when_clickable("//div[@class='search-results-module-next-page']",10)
                except TimeoutError:
                    finished = True


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
        

        
    

    
    
    
        

    

    