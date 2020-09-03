import os
from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

def uploader(qualifiers, upload_folder, target_site):
  driver = webdriver.Firefox()
  
  driver.get(target_site + '/login')

  proceed = input("Are you logged-in and ready to proceed? 'y' = yes, any key to abort: ")

  FILESDIR = upload_folder

  fileCount = sum([len(files) for r, d, files in os.walk(FILESDIR)])

  docCount = 0

  reconstitutedAltInfo = {}

    # with open(os.path.join(folder_location,'alt-info.txt')) as f:
    #     reconstitutedAltInfo = json.load(f)

  if proceed == 'y':
    for qualifier in qualifiers:
      for filename in os.listdir('./' + FILESDIR):
        if filename.endswith(qualifier):
          wait = WebDriverWait(driver, 300)
          if '.pdf' in qualifiers:
            driver.get(target_site + '/media/add/document')
            driver.find_element_by_id(
              "edit-field-document-0-upload").send_keys(os.getcwd() + '\\' + FILESDIR + '\\' + filename)
            )
            wait.until(presence_of_element_located(
              (By.NAME, 'field_document_0_remove_button')))
            driver.find_element(By.ID, 'edit-name-0-value').send_keys(filename)
            wait.until(element_to_be_clickable((By.XPATH, 'html/body/div[2]/div[1]/main/div[4]/div[1]/form/div[8]/input[@id="edit-submit"]')))
            docCount += 1

          if '.jpg' in qualifiers:
            driver.get(target_site + '/media/add/image')
            driver.find_element_by_id(
                "edit-image-0-upload").send_keys(os.getcwd() + '\\' + FILESDIR + '\\' + filename)
            wait.until(presence_of_element_located(
                (By.NAME, 'image_0_remove_button')))
