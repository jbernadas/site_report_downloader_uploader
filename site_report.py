import os
import sitemap_gen
from pprint import pprint
import requests
from lxml import etree

# Finds the generated .xml report inside ./site_report directory
def find_xml_report(directory):
  for file in os.listdir(directory):
    if file.endswith(".xml"):
      return file

# Counter - counts how many type of files based on qualifiers
def counter_func(qualifiers):
  xml_file = find_xml_report('.\site_report')
  doc = etree.parse('.\site_report\\' + xml_file)
  root = doc.getroot()
  counter = 0
  for i in range(0, len(root.getchildren())):
    for item in qualifiers:
      if (root[i][0]).text.endswith(item):
        counter += 1
  return counter

# Downloader - downloads either docs or images
def downloader(qualifiers, folder):
  session = requests.Session()
  xml_file = find_xml_report('.\site_report')
  doc = etree.parse('.\site_report\\' + xml_file)
  root = doc.getroot()
  count = 0
  count_type = counter_func(qualifiers)
  
  for i in range(0, len(root.getchildren())):
    for qualifier in qualifiers:
      if (root[i][0]).text.endswith(qualifier):
        filename = os.path.join(folder, root[i][0].text.split('/')[-1])
        with open(filename, 'wb') as im:
          im.write(session.get(root[i][0].text).content)
          count += 1
          print("Progress: {}/{}".format(count, count_type))
  session.close()
  print("Finished downloading {} files!".format(count))

# Where everything comes together
def main():
  targetSite = input("What is the target site? ")

  # get only first part of target site
  httpRemoved = targetSite.replace("https://", "")
  targetSplit = httpRemoved.split(".")[0]

  targetFolder = "./site_report/"

  # recreate original URL
  urlOrig = targetSite

  # only include web pages
  onlyWebPages = "-b tif -b mpg -b txt -b zip -b psd -b mpeg -b wmv -b mp3 -b xls -b gz -b tar -b png -b jpg -b jpeg -b gif -b mov -b mp4 -b xlsx -b doc -b docx -b pdf"

  # exclude tif mpg txt zip psd mpeg mp3 gz tar
  excludeThese = "-b tif -b mpg -b txt -b zip -b psd -b mpeg -b mp3 -b gz -b tar"

  # choose from the above variables what you want to include 
  include = excludeThese

  executeOrig = "python ./sitemap_gen.py {} -o {} {}".format(include, os.path.join(targetFolder, targetSplit) + ".xml", urlOrig)

  # run sitemap_gen.py on the original site
  os.system(executeOrig)

  DOCS_FOR_UPLOAD = '.\site_report\docs_for_upload'
  IMGS_FOR_UPLOAD = '.\site_report\imgs_for_upload'

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
  
  doc_count = counter_func(DOC_QUALIFIERS)
  img_count = counter_func(IMG_QUALIFIERS)

  print("Begin document download!")

  downloader(DOC_QUALIFIERS, DOCS_FOR_UPLOAD)

  print("----------")

  print("Begin image download!")

  downloader(IMG_QUALIFIERS, IMGS_FOR_UPLOAD)

if __name__ == "__main__":
  main()
