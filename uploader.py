import os
from bs4 import BeautifulSoup
import requests
import json
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

def uploader(target_site, qualifiers, upload_dir, alt_info_type, fileCount):
  driver = webdriver.Firefox()
  driver.get(target_site + '/login')

  proceed = input("Are you logged-in and ready to proceed? 'y' = yes, any key to abort: ")
  
  count = 0
  if proceed == 'y':
    for qualifier in qualifiers:
      for filename in os.listdir('./' + upload_dir):      
        wait = WebDriverWait(driver, 300)
        # if '.pdf' in qualifiers:
        #   driver.get(target_site + '/media/add/document')
        #   driver.find_element_by_id(
        #     "edit-field-document-0-upload").send_keys(os.getcwd() + '\\' + upload_dir + '\\' + filename)
        #   wait.until(presence_of_element_located(
        #     (By.NAME, 'field_document_0_remove_button')))
        #   driver.find_element(By.ID, 'edit-name-0-value').send_keys(filename)
        #   wait.until(element_to_be_clickable((By.XPATH, 'html/body/div[2]/div[1]/main/div[4]/div[1]/form/div[8]/input[@id="edit-submit"]')))
        #   count += 1

        #   print("Document upload progress: {}/{}".format(count, (fileCount -1)))
        #   continue
        
        # print("Finished uploading documents.")
        # count = 0
        print("Begin uploading images.")
        
        if '.jpg' in qualifiers:
          
          driver.get(target_site + '/media/add/image')
          driver.find_element_by_id(
              "edit-image-0-upload").send_keys(os.getcwd() + '\\' + upload_dir + '\\' + filename)
          wait.until(presence_of_element_located(
              (By.NAME, 'image_0_remove_button')))
          
          ### ALT-TEXT AUTO ###
          # If alt info, is properly enforced
          if alt_info_type.upper() == 'AUTO':
            if reconstitutedAltInfo.get(filename):
              alt_text = reconstitutedAltInfo.get(filename)
          # If alt info is shady, use image title
          if alt_info_type.upper() == 'TITLE':
            stripped_extension = filename.replace(qualifier, "")
            alt_text = stripped_extension.title()
          if alt_info_type.upper() == 'MANUAL':
            alt_text = input("What is the 'alt' text for this image? ")
          
          final_name = filename.replace("_", " ")
          final_name = final_name.replace("-", " ")
          driver.find_element_by_name(
              "image[0][alt]").send_keys(alt_text)
          driver.find_element(
              By.ID, "edit-name-0-value").send_keys(final_name)
          wait.until(element_to_be_clickable(
              (By.XPATH, 'html/body/div[2]/div[1]/main/div[4]/div[1]/form/div[10]/input[@id="edit-submit"]'))).click()
          count += 1
          
          print("Image upload progress: {}/{}".format(count, (fileCount -1)))
    
          continue
    driver.quit()
  else:
    driver.quit()

def main():
  target_site = input("Website URL to upload to: ")
  url_parsed = urlparse(target_site)
  site_name = url_parsed.hostname.split('.')[0]
  site = site_name.replace('-prod', '')

  upload_root = 'site_report\\' + site

  DOCS = upload_root + '\\' + 'docs_for_upload'
  IMGS = upload_root + '\\' + 'imgs_for_upload'
  
  docFileCount = sum([len(files) for r, d, files in os.walk(DOCS)])
  imgFileCount = sum([len(files) for r, d, files in os.walk(IMGS)])

  reconstitutedAltInfo = {}

  with open(os.path.join(upload_root,'alt-info.json')) as f:
      reconstitutedAltInfo = json.load(f)

  DOC_QUALIFIERS = [
    '.pdf',
    '.doc',
    '.docx',
    '.xls',
    '.xlsx'
  ]

  IMG_QUALIFIERS = [
    '.jpg',
    '.png',
    '.gif'
  ]

  uploader(target_site, DOC_QUALIFIERS, DOCS, None, docFileCount)
  uploader(target_site, IMG_QUALIFIERS, IMGS, "title", imgFileCount)
  

if __name__ == "__main__":
  main()
