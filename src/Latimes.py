from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import requests #only to download picture from a url

import re
import os
from typing import List
from datetime import datetime

from src.Sheets import Sheets_Manipulation
from datetime import datetime
from dateutil.relativedelta import relativedelta

class LatimesExtractor:
    def __init__(self,count_news: int, phrase, sort_by, date) -> None:
        """Initializing class of website"""
        self.browser = Selenium()
        self.table = Tables()
        self.count_news = count_news
        self.date = int(date)
        self.phrase = phrase
        self.sort_by = sort_by
        self.sheet = Sheets_Manipulation()
        self.sheet.create_file()
        self.sheet.delete_worksheet_if_exists(self.phrase)

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
        without_data = False
        while (finished == False or count_news_found < self.count_news) and without_data==False:
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
                        if "not found" in picture_file_name:
                            picture_path = "Erro to download - File Without Extension"
                        else:
                            picture_path = self.download_news_picture(picture_link, picture_file_name)
                        href = new.find_element(By.TAG_NAME, "a").get_attribute("href")
                        if not self.verify_date(date) == True:
                            print("There are no more messages in the established retroactive months")
                            without_data = True
                            finished = True
                            break
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
                        count_phrases_title, count_phrases_description = self.count_phrases(title, description) 
                        money_appears = self.extract_money_amounts(title, description)
                        self.sheet.create_worksheet(self.phrase)
                        self.sheet.add_row_in_worksheet(self.phrase, [title, topic, date, description, picture_path, count_phrases_title, count_phrases_description, str(money_appears), href])
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
        
    def verify_date(self, date_extracted):
        months = self.date
        retroactive_months = []
        retroactive_years = []
        if months >= 1:
            months-=1
        while True:
            last_month = datetime.now() - relativedelta(months=months)
            month_name = last_month.strftime("%b")
            year = last_month.year
            retroactive_months.append(month_name)
            retroactive_years.append(year)
            months -=1
            if months < 0:
                break
        if "ago" in date_extracted:
            return True
        else:
            for index, month in enumerate(retroactive_months):
                if str(month) in str(date_extracted) and str(retroactive_years[index]) in str(date_extracted):
                    return True
            return False

    def count_phrases(self, title, description):
        count_in_title = title.lower().count(self.phrase.lower())
        count_in_description = description.lower().count(self.phrase.lower())
        return count_in_title, count_in_description

    def extract_money_amounts(self, title, description):
        text = title + description
        patterns = [
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?', # Matches $ amounts, e.g., $11.1, $111,111.11
            r'\d+(?:,\d{3})*\s*dollars', # Matches amounts in dollars, e.g., 11 dollars
            r'\d+(?:,\d{3})*\s*USD' # Matches amounts in USD, e.g., 11 USD
        ]
        money_amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            money_amounts.extend(matches)
        if len(money_amounts)>=1:
            return True
        return False
    
    def download_news_picture(self, src, picture_name):
        directory_path = "output/pictures"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        path = f"{directory_path}/{picture_name}"
        links = src.split(",")
        link = links[len(links)-1][:-5]
        print(link)
        response = requests.get(link)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded and saved as '{path}'.")
        else:
            print("Failed to retrieve the image. Status code:", response.status_code)

        return path
