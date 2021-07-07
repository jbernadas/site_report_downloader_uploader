from bs4 import BeautifulSoup
import requests
import sys
import lxml
import re
from urllib.parse import urlparse
from urllib.parse import urljoin

target_folder = ""

searched_links = []

broken_links = []

def getLinksFromHTML(html):
  def getLink(el):
    return el["href"]
  return list(map(getLink, BeautifulSoup(html, 'lxml').select('a[href]')))

def find_broken_links(domainToSearch, URL, parentURL):
  global target_folder 

  target_folder = domainToSearch.split('.')[0]

  target_urls_file = open('./site_report/' + target_folder + '/' + target_folder + '-urls.txt', 'r')

  target_urls_content = target_urls_file.read().replace('\n', ',')

  target_urls = target_urls_content.split(',')

  target_urls_file.close()

  if (not (URL in searched_links)) and (not URL.startswith("mailto:")) and (not ("javascript:" in URL)) and (not URL.endswith(".pdf")):
    try:
      requestObj = requests.get(URL)
      parsedObj = urlparse(URL)
      searched_links.append(URL)
      # dont_parse = {'.pdf', '.doc', '.pptx', '.docx', '.jpg', '.png', '.gif', '.xls', '.xlsx', '.mov', '.mp3', '.mp4'}
      if (requestObj.status_code == 404):
        broken_links.append("BROKEN: link " + URL + "\nfrom " + parentURL)
        print(broken_links[-1])
      # if(parsedObj.netloc == 'nda.llnl.gov'):
      #   broken_links.append("OLD: link " + URL + "\nfrom" + parentURL)
      if '-prod' in parsedObj.netloc:
        if parsedObj.netloc == targetSplit.replace('-prod', '') :
          broken_links.append("OLD: link " + URL + "\nfrom " + parentURL)
      else:
        print("NOT BROKEN: link " + URL + " from " + parentURL)
        if urlparse(URL).netloc == domainToSearch:
          for link in getLinksFromHTML(requestObj.text):
            # for item in dont_parse:
            #   if link.endswith(item):
            #     print('Link ends with {}, skipping.'.format(item))
            #     pass
            find_broken_links(domainToSearch, urljoin(URL, link), URL)
              
    except requests.exceptions.ConnectionError as e:
      requestObj = "No response"
      searched_links.append(domainToSearch)

def main():

  find_broken_links(urlparse(sys.argv[1]).netloc, sys.argv[1], "")

  global target_folder

  print("\n--- DONE! ---\n")

  with open('./site_report/' + target_folder + '/broken-links.txt', 'w') as f:
    for link in broken_links:
      f.write("{}\n\n".format(link))

if __name__ == "__main__":
  main()
