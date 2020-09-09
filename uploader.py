# This is a document uploader script.
# You have to have the same version-as-your-browser
# Firefox GeckoDriver to use this. You have to install
# those separately from pip, and needs to be added to PATH.

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

help_text = """uploader.py version 0.0.1 (2020-09-08)
    This custom script uploads files to a target Drupal website.
    
    Command line syntax:

    python uploader.py <options> <URL you are uploading to>

    Available options:
    -h         --help                Print this text and exit

    -b <ext>   --block <ext>         Exclude URLs with the given extension;
                                    <ext> must be without the leading dot.
                                    The comparison is case insensitive, so
                                    for example DOC and doc are treated
                                    the same. You can use this option several
                                    times to block several extensions.

    -c <value> --changefreq <value>  Set the change frequency. The given value
                                    is used in all sitemap entries (maybe a
                                    future version of this script will change
                                    that). The allowed values are: always,
                                    hourly, daily, weekly, monthly, yearly,
                                    never.

    -p <prio>  --priority <prio>     Set the priority. The value must be from
                                    the interval between 0.0 and 1.0. The value
                                    will be used in all sitemap entries.

    -m <value> --max-urls <value>    Set the maximum number of URLs to be crawled.
                                    The default value is 1000 and the largest
                                    value that you can set is 50000 (the script
                                    generates only a single sitemap file).

    -r <value> --ratelimit <value>   Set a crawl rate limit [requests / second],
                                    zero (the default) results in no crawl rate
                                    limitation.

    -o <file>  --output-file <file>  Set the name of the geneated sitemap file.
                                    The default file name is sitemap.xml.

    Usage example:

    python3 uploader.py -t doc http://target-prod.llnl.gov

"""
def uploader():
    # Initialize webdriver. We are using Firefox because Chrome is spotty on the login bit.
    driver = webdriver.Firefox()

    # Target base URL
    target_site = input("What is the name of the website? ")

    # Strips the leading 'https://' from target_site
    parsedUrl = urlparse(target_site)

    # Strips the following '.llnl.gov'
    site_name = parsedUrl.hostname.split('-')[0]
    
    # Login to site manually
    driver.get(target_site + '/login')

    # Ask if user has logged-in to site and ready to proceed
    proceed = input(
        "Are you logged-in and ready to proceed? 'y' = yes, any key to abort: ")

    # The directory where our soon-to-be uploaded documents reside
    FILESDIR = "site_report\\" + site_name + "\\docs_for_upload"

    fileCount = sum([len(files) for r, d, files in os.walk(FILESDIR)])

    # List of file types we are looking to upload
    
    count = 0
    ### Our uploader script ###

    # For each qualifier in list of QUALIFIERS
    for qualifier in QUALIFIERS:
        # for each filename inside our document directory
        for filename in os.listdir('./' + FILESDIR):
            # and if filename ends with the qualifier being iterated
            if filename.endswith(qualifier):
                # initialize a wait variable that makes the driver wait for so many seconds
                wait = WebDriverWait(driver, 120)
                # go to the /media/add/document of the Drupal site
                driver.get(target_site + "/media/add/document")
                # look for the id of input area and fill it with the path to our file-to-upload
                driver.find_element_by_id(
                    "edit-field-document-0-upload").send_keys(os.getcwd() + '\\' + FILESDIR + '\\' + filename)
                # wait until the page is finished uploading, in this case 
                # when the remove button appears, before proceeding
                wait.until(presence_of_element_located(
                    (By.NAME, 'field_document_0_remove_button')))
                # look for the 'name' input box and fill it with the same name as the file
                driver.find_element(
                    By.ID, "edit-name-0-value").send_keys(filename)
                # wait for the 'save' button to appear, then click it.
                wait.until(element_to_be_clickable(
                    (By.XPATH, 'html/body/div[2]/div[1]/main/div[4]/div[1]/form/div[8]/input[@id="edit-submit"]'))).click()
                # rinse, repeat.
                count += 1

                print("Upload progress: {}/{}".format(count, (fileCount)))
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

    ]

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.stderr.write(help_text)
            return 1
        elif opt in ("-t", "type="):
            fileType = arg
            if fileType == (arg.upper() == "DOC"):
                fileType = DOC_QUALIFIERS
            if fileType == (arg.upper() == "IMG"):
                fileType = IMG_QUALIFIERS
            if fileType in ("", ".", ".."):
                sys.stderr.write("Please provide a sensible file name.\n")
                return 1
    if not args:
        sys.stderr.write("You must provide the target URL to upload to.")

    ## Fire up the uploader
    uploader()

if __name__ == "__main__":
    try:
        status_code = main()
    except KeyboardInterrupt:
        status_code = 130
    sys.exit(status_code)
