#! /usr/bin/env python3
"""
    Copyright (C) 2020 Joseph Bernadas

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

# This is a document uploader script.
# You have to have the same version-as-your-browser
# Firefox GeckoDriver to use this. You have to install
# that separately from pip, and needs to be added to PATH.

import getopt
import os
from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

help_text = """
    ####################################################
    ####   UPLOADER.py version 0.0.1 (2020-09-08)   ####
    ####################################################

    This command line program uploads files to a target Drupal website.
    
    Command line syntax:

    python uploader.py <options> <URL you are uploading to> 

    Available options:
    -h         --help                       Print this text and exit

    -t <doc or img> --type <doc or img>     Type of files you want to upload;
                                            choices are either 'doc' or 'img' (without the quotes).
                                            The case is insensitive, so for example DOC and doc are treated
                                            the same. You can use this option once.

    Usage example:

    python3 uploader.py -t doc http://target-prod.llnl.gov

"""
def uploader(QUALS, TARGET_SITE):
    # Initialize webdriver. We are using Firefox because Chrome is spotty on the login bit.
    driver = webdriver.Firefox()

    # # Target base URL
    target_site = TARGET_SITE

    # Strips the leading 'https://' from target_site
    parsedUrl = urlparse(target_site)

    # Strips the following '.llnl.gov'
    site_name = parsedUrl.hostname.split('-')[0]
    
    # Login to site manually
    driver.get(target_site + '/login')

    # # Ask if user has logged-in to site and ready to proceed
    proceed = input("Are you logged-in and ready to proceed? 'y' = yes, any key to abort: ")

    # List of file types we are looking to upload
    DOC_QUALIFIERS = [
        '.pdf',
        '.docx',
        '.txt',
        '.doc',
        '.wrf',
        '.xls',
        '.xlsx'
        # '.tar',
        # '.tgz',
        # '.gz',
        # '.bz2'
    ]

    IMG_QUALIFIERS = [
        '.jpg',
        '.jpeg',
        '.png',
        '.gif'
    ]

    QUALIFIERS = []

    # Target folder
    folder_location = "site_report\\" + site_name

    # The directory where our soon-to-be uploaded documents reside
    FILESDIR = ""

    if QUALS.upper() == "DOC":
        QUALIFIERS = DOC_QUALIFIERS
        FILESDIR = folder_location + "\\docs_for_upload"

    if QUALS.upper() == "IMG":
        QUALIFIERS = IMG_QUALIFIERS
        FILESDIR = folder_location + site_name + "\\imgs_for_upload"
    

    fileCount = sum([len(files) for r, d, files in os.walk(FILESDIR)])

    count = 0

    # initialize a wait variable that makes the driver wait for so many seconds
    wait = WebDriverWait(driver, 120)

    reconstitutedAltInfo = {}

    with open(os.path.join(folder_location, 'alt-info.txt')) as f:
        reconstitutedAltInfo = json.load(f)

    # For each qualifier in list of QUALIFIERS
    for qualifier in QUALIFIERS:
        # for each filename inside our document directory
        for filename in os.listdir('./' + FILESDIR):
            # and if filename ends with the qualifier being iterated and it contains a .PDF file
            if filename.endswith(qualifier) and '.pdf' in QUALIFIERS:
                # Go to the /media/add/document of the Drupal site
                driver.get(target_site + "/media/add/document")
                # Look for the id of input area and fill it with the path to our file-to-upload
                driver.find_element_by_id(
                    "edit-field-document-0-upload").send_keys(os.getcwd() + '\\' + FILESDIR + '\\' + filename)
                # Wait until the page is finished uploading, in this case \ 
                # when the remove button appears, before proceeding
                wait.until(presence_of_element_located(
                    (By.NAME, 'field_document_0_remove_button')))
                # Looks for the 'name' input box and fill it with the same name as the file
                driver.find_element(
                    By.ID, "edit-name-0-value").send_keys(filename)
                # Wait for the 'save' button to appear, then robot clicks it.
                wait.until(element_to_be_clickable(
                    (By.XPATH, 'html/body/div[2]/div[1]/main/div[4]/div[1]/form/div[8]/input[@id="edit-submit"]'))).click()
                # rinse, repeat.
                count += 1

                print("Upload progress: {}/{}".format(count, (fileCount)))
                continue

            if filename.endswith(qualifier) and '.jpg' in QUALIFIERS:
                print(filename)
                driver.get(target_site + "/media/add/image")
                driver.find_element_by_id("edit-image-0-upload").send_keys(os.getcwd() + '\\' + FILESDIR + '\\' + filename)
                wait.until(presence_of_element_located((By.NAME, 'image_0_remove_button')))

                ### ALTERNATIVE TEXT HANDLER ###
                ##  Uncomment the below options to control how alt text for each image is populated

                ##  Manual  ## 
                # user_inputted_alt_text = input("What would you like to put as 'alt' text for {}? ".format(filename))
                # alt_text = user_inputted_alt_text

                ##  Filename Based ##
                # strip_extension = filename.replace(qualifier, "")
                # underscore_to_space = strip_extension.replace("_", " ")
                # alt_text = underscore_to_space.replace("-", " ")

                ##  Automated  ##
                ## if filename has corresponding alt text use it
                if reconstitutedAltInfo.get(filename):
                    alt_text = reconstitutedAltInfo
                ## otherwise
                else:
                    ## use filename as alt text
                    strip_extension = filename.replace(qualifier, "")
                    underscore_to_space = strip_extension.replace("_", " ")
                    alt_text = underscore_to_space.replace("-", " ")
                
                ## Name field cleaner
                final_name = filename.replace("_", " ")
                final_name = final_name.replace("-", " ")

                ## Fill in the alt text input field
                driver.find_element_by_name("image[0][alt]").send_keys(alt_text)

                ## Fill in the name input field
                driver.find_element(By.ID, "edit-name-0-value").send_keys(final_name)
                
                ## Wait until button is clickable, then click it
                wait.until(element_to_be_clickable((By.XPATH, 'html/body/div[2]/div[1]/main/div[4]/div[1]/form/div[10]/input[@id="edit-submit"]'))).click()
                continue

    print('Upload complete! {} of {} documents uploaded.'.format(count, (fileCount)))
    print('\a')
    # Exit the driver.
    driver.quit()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht", ["help", "type="])

    except getopt.GetoptError:
        sys.stderr.write(help_text)
        return 1

    QUALS = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.stderr.write(help_text)
            return 1
        elif opt in ("-t", "type="):
            QUALS = arg
            if QUALS == (arg.upper() == "DOC"):
                QUALS = DOC_QUALIFIERS
            if QUALS == (arg.upper() == "IMG"):
                QUALS = IMG_QUALIFIERS
            if QUALS in ("", ".", ".."):
                sys.stderr.write("Please provide a qualifier type. Choices are 'doc' or 'img'.\n")
                return 1
    if not args:
        sys.stderr.write("You must provide the target URL to upload to.")
        return 1

    ## Fire up the uploader
    uploader(args[0], args[1])

if __name__ == "__main__":
    try:
        status_code = main()
    except KeyboardInterrupt:
        status_code = 130
    sys.exit(status_code)
