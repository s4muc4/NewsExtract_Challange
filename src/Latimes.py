from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables

from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

import re
import os
from typing import List
from datetime import datetime
from src.Sheets import Sheets_Manipulation
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.Logging import Log_Message
from textblob import TextBlob

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
        self.log = Log_Message()
        self.path = "output/pictures"

    def open_specific_browser(self,url) -> None:
        """This function open los angeles times website"""
        self.log.log_info(f"Acessing {url}")
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.browser.open_browser(url=url, options=opts)

    def close_browser(self) -> None:
        """This function close los angeles times website"""
        self.log.log_info("Closing browser")
        self.browser.close_all_browsers()

    def search_by_phrase(self) -> int:
        """This function search news by a phrase in workitem and get count of results"""
        try:
            self.log.log_info("#######################################################################################################################")
            self.log.log_info(f"Searching phrase ({self.phrase}) in order by ({self.sort_by}) since ({self.date}) months")
            self.log.log_info("#######################################################################################################################")
            self.browser.click_button("//button[@data-element='search-button']")
            self.browser.input_text("//input[@data-element='search-form-input']", self.phrase)
            self.browser.press_keys(None, "RETURN")
            self.log.log_info("Getting count of results")
            self.browser.wait_until_element_is_enabled("//span[@class='search-results-module-count-desktop']","15")
            result = self.browser.get_text("//span[@class='search-results-module-count-desktop']")
            regex_numbers = re.findall(r'\d+', result)
            news_count = ''.join(regex_numbers)
            self.browser.wait_until_element_is_enabled("//select[@class='select-input']","30")
            try:
                self.browser.select_from_list_by_label("//select[@class='select-input']",self.sort_by)
            except Exception as err:
                self.browser.select_from_list_by_label("//select[@class='select-input']","Relevance")
            self.log.log_info(str(news_count) +" - results." )
        except Exception as err:
            self.browser.wait_until_element_is_enabled("//div[@class='search-results-module-no-results']","30")
            news_count = self.browser.get_text("//div[@class='search-results-module-no-results']")
            self.log.log_warn(news_count)
        try:
            return int(news_count)
        except Exception:
            return 0
    
    def get_page_news(self) -> tuple[bool, str]:
        """
        Get some informations like title, description and date of each news on screen.
        If all the information was taken, some business rules are validated, like if date is on range of months.
        Get word counts in title and description, and get if money appears in title or description
        Finally, call Sheet functions to save informations in a Excel file.
        """
        try:
            count_news_found = 0
            finished = False
            without_data = False
            while (finished == False or count_news_found < self.count_news) and without_data==False:
                self.log.log_info("Get all news from result page")
                self.sheet.create_worksheet(self.phrase)
                news:List[WebElement] = self.browser.get_webelements("//ul[@class='search-results-module-results-menu']/li/ps-promo") 
                for new in news:
                    if count_news_found < self.count_news: 
                        try:
                            title = new.find_element(By.CLASS_NAME, "promo-title").text
                            topic = new.find_element(By.XPATH, "//p[@class='promo-category']/a").text
                            date = new.find_element(By.CLASS_NAME, "promo-timestamp").text
                            description = new.find_element(By.CLASS_NAME, "promo-description").text
                            sentiment = TextBlob(description)
                            polarity = sentiment.polarity
                            subjectivity = sentiment.subjectivity
                            picture_link = new.find_element(By.CLASS_NAME, "image").get_attribute("srcset")
                            #picture_src = new.find_element(By.CLASS_NAME, "image")
                            picture_file_name = self.get_image_file_name(picture_link)
                            if "not found" in picture_file_name:
                                picture_path = "Error to download - File Without Extension"
                            else:
                                picture_path = self.download_news_picture(picture_link, picture_file_name)
                            href = new.find_element(By.TAG_NAME, "a").get_attribute("href")
                            if not self.verify_date(date) == True and count_news_found == 0:
                                self.sheet.delete_worksheet_if_exists("Sheet1")
                                msg = "There are no more messages in the established retroactive months"
                                self.log.log_info(msg)
                                return False, str(msg)
                            count_news_found += 1
                            self.log.log_info("-----------------------------------------------------------------------------------------------------------------------")
                            self.log.log_info("New number: " + str(count_news_found))
                            self.log.log_info("Title: "+title)
                            self.log.log_info("Topic: "+topic)
                            self.log.log_info("Post Date: "+date)
                            self.log.log_info("Description: "+description)
                            self.log.log_info("Picture file name: "+picture_file_name)
                            self.log.log_info("URL of new: "+href)
                            self.log.log_info("-----------------------------------------------------------------------------------------------------------------------")
                            self.log.log_info("Extracting phrases count")
                            count_phrases_title, count_phrases_description = self.count_phrases(title, description) 
                            self.log.log_info("Extracting money")
                            money_appears = self.extract_money_amounts(title, description)
                            self.log.log_info("Creating worksheet if doesn't exists")
                            self.log.log_info("Adding row into a excel file")
                            self.sheet.add_row_in_worksheet(self.phrase, [title, topic, date, description, picture_path, count_phrases_title, count_phrases_description, str(money_appears), href, polarity, subjectivity])
                        except Exception as err:
                            self.log.log_info("Error to get new from " + self.phrase)
                    else:
                        finished = True
                if finished == False:
                    try:
                        self.browser.click_element_when_clickable("//div[@class='search-results-module-next-page']",10)
                    except TimeoutError:
                        finished = True
        except Exception as err:
            return False, str(err)
        finally:
            self.sheet.delete_worksheet_if_exists("Sheet1")
        return True, "OK"

    def get_image_file_name(self, srcset) -> str:
        """
        Get picture file name from news
        """
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
            self.log.log_info(filename)
        else:
            self.log.log_info("Picture filename: " + filename)
        return filename
        
    def download_news_picture(self, src, picture_name)-> str:
        """
        Download news picture and save in output folder (output/pictures)
        It's necessary open an auxiliary window to take a screenshot of the image in big size.
        """
        directory_path = self.path
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        links = src.split(",")
        link = links[len(links)-1][:-5]
        self.log.log_info(f"Link of picture: {link}" )
        self.browser.execute_javascript("window.open('');")
        window_handles = self.browser.get_window_handles()
        self.browser.switch_window(window_handles[1])
        self.browser.go_to(link)
        path = f'{self.path}/{picture_name}'
        self.browser.screenshot("//img", path)
        self.browser.close_window()
        self.browser.switch_window(window_handles[0])
        return path

    def verify_date(self, date_extracted) -> bool:
        """
        Verify if news date are on the range of months suggested by workitem
        Return: boolean
        """
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

    def count_phrases(self, title, description) -> tuple[str, str]:
        """
        Count how many word matches appears in title, and description
        """
        count_in_title = title.lower().count(self.phrase.lower())
        count_in_description = description.lower().count(self.phrase.lower())
        return str(count_in_title), str(count_in_description)

    def extract_money_amounts(self, title, description) -> bool:
        """
        Do a regex in title and description to get money amount. If some amont money appears, the function returns True
        Return: boolean
        """
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