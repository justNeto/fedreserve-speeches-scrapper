#!/usr/bin/env python

import os
import re
import time

# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ExpectedConditions

from datetime import datetime
'''
Selenium wrapper class for simplicity
'''
class SeleniumOptions():

    def __init__(self, browser="Chrome", headless=False, speaker="powell"):

        self._speakers = {
                "powell": 1,
                "jefferson": 2,
                "barr": 3,
                "bowman": 4,
                "cook": 6,
                "kugler": 7,
                "waller": 8,
                "former": 9,
                "other": 10
        }

        self.speaker = speaker
        self.headless = headless
        self.browser = browser
        self.driver = None

        # Instance a selenium options object to return
        try:
            if self.browser == "chrome":
                self.selenium_options = webdriver.ChromeOptions()
                self.driver = webdriver.Chrome()
            elif self.browser == "firefox":
                self.selenium_options = webdriver.FirefoxOptions()
                self.driver = webdriver.Firefox()
            else:
                raise AttributeError(
                    f"wrong browser specified"
                )

            if self.headless is True:
                self.selenium_options.add_argument("--headless")
            elif self.headless is False:
                pass
            else:
                raise

            if self.config.window_size:
                self.selenium_options.set_window_size(1872, 1344)

        except:
            pass


    def get_driver(self):
        return self.driver, self._speakers[self.speaker], self.speaker


class TestGetPowellsLinks():

    def __init__(self):
        self.speech_links = list()
        self.nth_child = None
        self.target = None

    # Sanitize the file name to remove invalid characters
    def sanitize_filename(self, filename):
        # Remove characters that are not allowed in Windows file names
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def generate_document(self, link):

        try:
            self.driver.get(link)
            print(f"::-> Generate document for link {link}")

            # Wait until the article element is loaded
            article_element = WebDriverWait(self.driver, 10).until(
                ExpectedConditions.presence_of_element_located((By.CLASS_NAME, "title"))
            )

            try:
                date_data = self.driver.find_element(By.CLASS_NAME, "article__time").text
            except:
                raise ValueError(
                    f"date data inexistent"
                )

            try:
                title_data = self.driver.find_element(By.CLASS_NAME, "title").text
            except:
                raise ValueError(
                    f"title data inexistent"
                )

            try:
                speaker_data = self.driver.find_element(By.CLASS_NAME, "speaker").text
            except:
                raise ValueError(
                    f"speaker data inexistent"
                )

            try:
                location_data = self.driver.find_element(By.CLASS_NAME, "location").text
            except:
                raise ValueError(
                    f"location data inexistent"
                )

            try:
                content_paragraphs = self.driver.find_elements(By.ID, "article")
                content_text = "\n".join([para.text for para in content_paragraphs])
            except:
                raise ValueError(
                    f"content data inexistent"
                )

            # Combine all extracted information into one text block
            article_data = f"Date: {date_data}\n\nTitle: {title_data}\n\nSpeaker: {speaker_data}\n\nLocation: {location_data}\n\n{''.join(content_text)}"
            print(f"::-> Generating article <-::\n")
            sanitized_date = datetime.strptime(date_data, "%B %d, %Y").strftime("%m_%d_%Y")
            sanitized_title = self.sanitize_filename(title_data)

            sanitized_file_name = sanitized_title + "_" + sanitized_date
            
            # Save to a file
            file_name = f'{sanitized_file_name.replace(" ", "_")}.txt'  # Ensure valid file name
            data_path = os.path.join(os.path.abspath(os.getcwd()), "data")  # Cross-platform path handling

            if not os.path.exists(data_path):
                os.makedirs(data_path)

            with open(os.path.join(data_path, file_name), 'w', encoding='utf-8') as fp:
                fp.write(article_data)

        except Exception as e:
            print(f"::!-> Error occurred:\n {e}")
            raise e


    def select_target(self):
        self.driver.get("https://www.federalreserve.gov/newsevents/speeches.htm")
        seach_string = ".checkbox:nth-child(" + str(self.nth_child) + ") .ng-scope"
        self.driver.find_element(By.CSS_SELECTOR, seach_string).click()
        self.driver.find_element(By.CSS_SELECTOR, ".icon-more").click()


    def extract_speeches_links(self):
        base_string = "^https://www.federalreserve.gov/newsevents/speech/"
        a_elements = self.driver.find_elements(By.XPATH, "//a[@href]")

        if self.target == "former" or self.target == "other":
            speaker_element = self.driver.find_element(By.XPATH, "//p[@class='news__speaker ng-binding']")
            speaker_name = speaker_element.text
            name_parts = speaker_name.split()
            last_name = name_parts[-1]  # should get the last name
            print(f"::-> Last Name found: {last_name}")

            re_match_string = base_string + last_name + ".*$"
        else:
            re_match_string = base_string + self.target + ".*$"

        for element in a_elements:
            if re.match(re_match_string, element.get_attribute("href")):
                self.speech_links.append(element.get_attribute("href"))


    def setup_method(self, options):
        self.driver, self.nth_child, self.target  = options.get_driver()
        self.vars = {}


    def teardown_method(self):
        self.driver.quit()


    def run(self):
        self.select_target()

        # Find the pagination <ul> element
        pagination_ul = self.driver.find_element(By.XPATH, "//ul[@uib-pagination]")

        # Find all the <a> elements inside the pagination <ul> (these represent the page numbers)
        page_links = pagination_ul.find_elements(By.TAG_NAME, "a")

        # Capture the number of pages in the pagination (max size is 4, but you can confirm the number of visible links)
        total_pages = len(page_links) - 2

        # Print out the number of pages for debugging
        print(f"::-> Total Pages: {total_pages}")

        current_page = 1

        while current_page < total_pages:
            try:

                # Scrape data on the current page
                time.sleep(1)

                print(f"::-> Extracting page link from page {current_page}")
                self.extract_speeches_links()

                next_button = self.driver.find_element(By.XPATH, "//li[contains(@class, 'pagination-next')]//a[text()='Next']")
                next_button.click()
                current_page += 1

            except Exception as e:
                print(f"::!->\n Error occurred: {e}")
                break  # Exit the loop if there is an error (e.g., no "Next" button found)

        print(f"::-> Speeches found:\n {self.speech_links} \n\n <-::")

        try:
            # Extract all data using the list
            for link in self.speech_links:
                self.generate_document(link)

            self.teardown_method()
        except Exception as e:
            self.teardown_method()


if __name__ == '__main__':
    speeches = TestGetPowellsLinks()
    options = SeleniumOptions(browser="firefox", headless=True, speaker="powell")
    speeches.setup_method(options)
    speeches.run()
