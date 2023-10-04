# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import csv
from playwright.sync_api import Playwright, sync_playwright

HTML_SAVE_PATH = "/Users/CHJ/文稿/crawler_simpleform/html/" # Input the path you want to save all files into
DATABASE_URL = "https://www.wise-agent.com/database/" # Input the url you want to scrape
DATABASE_NAME = "wise-agent" # Set name of database for scraping
ENCODING_FORMAT = "utf-8"
MAIN_CONTENT_CLASS = "main-content-box clearfix" # The class of main content of target

def get_html_of_database(DATABASE_URL, DATABASE_NAME) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(DATABASE_URL)
        database_html = page.content() # Get the html of database
        with open(HTML_SAVE_PATH + DATABASE_NAME + '.html', 'w', encoding=ENCODING_FORMAT) as f:
            f.write(database_html) # Save the html of database as 'DATABASE_NAME.html'
        page.close()

def get_fraud_info(HTML_SAVE_PATH, DATABASE_NAME) -> None:
    with open(HTML_SAVE_PATH + DATABASE_NAME + '.html', 'r', encoding=ENCODING_FORMAT) as f:
        database_html_doc = f.read()
    soup = BeautifulSoup(database_html_doc, 'html.parser')
    all_url = set() # Use set to avoid the repetition of urls
    main_content = soup.find('div', attrs={"class": MAIN_CONTENT_CLASS}) # Get the div in main-content because it contains all urls to be crawled
    links = main_content.find_all('a')
    for link in links:
        all_url.add(link['href']) # Get all urls to be crawled
    with open(HTML_SAVE_PATH+'all_urls_to_be_crawled'+'.html', 'w', encoding=ENCODING_FORMAT) as f:
        f.write('\n'.join(all_url)) # Save all urls to be crawled as 'all_urls_to_be_crawled.html', just for checking
    with open(HTML_SAVE_PATH + DATABASE_NAME +'.csv', 'w', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file) # Create a csv file to save the fraud info
        writer.writerow(["URL", "タイトル", "詐欺種別", "名称等", "所在地", "代表者", "電話番号", "E-mail", "被害内容"])
        for fraud_info_link in list(all_url): # Crawl the fraud info from all urls
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.goto(fraud_info_link)
                fraud_info_html_content = page.content()
                soup = BeautifulSoup(fraud_info_html_content, 'html.parser')
                fraud_info = soup.find('div', id='main-content') # Extract the fraud info from the html
                # Get the fraud info
                all_td_tag = fraud_info.find_all('td')
                fraud_info_url = fraud_info_link
                fraud_info_title = fraud_info.select_one('div.post-title > div:last-child').text
                fraud_info_category = all_td_tag[0].text
                fraud_info_name = all_td_tag[1].text
                fraud_info_address = all_td_tag[2].text
                fraud_info_representative = all_td_tag[3].text
                fraud_info_phone_number = all_td_tag[4].text
                fraud_info_email = all_td_tag[5].text
                fraud_info_frauded_content = all_td_tag[7].text.replace('\n', '\\n') # Replace '\n' with '\\n' to avoid the error of inputting csv file
                # Write the fraud info into csv file
                writer.writerow([fraud_info_url, fraud_info_title, fraud_info_category, fraud_info_name, fraud_info_address, fraud_info_representative, fraud_info_phone_number, fraud_info_email, fraud_info_frauded_content])

if __name__ == "__main__":
    get_html_of_database(DATABASE_URL, DATABASE_NAME)
    get_fraud_info(HTML_SAVE_PATH, DATABASE_NAME)

