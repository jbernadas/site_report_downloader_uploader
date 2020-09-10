
## A custom script specifically created for counting 
## all uploaded images inside a Drupal website.

import os
import itertools
from bs4 import BeautifulSoup
import requests
import sys
import lxml
from urllib.parse import urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

def img_counter():
    ## Initialize webdriver. We are using Firefox because Chrome is spotty on the login bit.
    driver = webdriver.Firefox()

    ## Target base URL
    target_site = input("What is the name of target site? ")

    ## Strips the leading 'https://' from target_site
    parsedUrl = urlparse(target_site)

    ## Strips the following '.llnl.gov'
    site_name = parsedUrl.hostname.split('-')[0]
    
    ## Login to site manually
    driver.get(target_site + '/login')

    ## Ask if user has logged-in to site and ready to proceed
    proceed = input("Are you logged-in and ready to proceed? 'y' = yes, any key to abort: ")

    site_img_page = "/admin/content/files?filename=&filemime=image/&status=All"

    driver.get(target_site + site_img_page)

    last_img_page = driver.find_element_by_css_selector("li.pager__item--last a")

    max_count = last_img_page.get_attribute("href").split("=")[-1]

    img_page = target_site + site_img_page
    
    count = 0
    img_count = 0

    imgs = []
    
    # session = requests.session()
    # session.keep_alive = False

    for i in range(0, int(max_count) + 1):
      try:
        driver.get("{}&page={}".format(img_page, count))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        target_tds = soup.find_all('td', attrs={'class': 'views-field-filename'})
        for td in target_tds:
          print(td.a['href'].split('/')[-1])
          img_count += 1   
        count += 1
      except:
        driver.close()
    
    print("There are {} images in this website.".format(img_count))
    driver.close()

def main():
  img_counter()

if __name__ == "__main__":
  main()
