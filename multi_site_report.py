import site_report
from urllib.parse import urlparse
import os

def main():

  urls = []

  with open('url_list.txt', 'r') as f:
    for line in f:
      url_list = [elt.strip() for elt in line.split(',')]
      for item in url_list:
        urls.append(item)

  for url in urls:
    print(url)
    # parseUrl = urlparse(url)

    execute_site_report_py = "python ./site_report.py -d no {}".format(url)

    os.system(execute_site_report_py)

if __name__=='__main__':
  main()
