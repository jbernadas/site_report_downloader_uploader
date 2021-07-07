import re

fileName = "app-urls.xml"

# if fileName.upper().endswith(".TXT"):
#   print("Text file detected!")
# if fileName.upper().endswith(".XML"):
#   print("XML file detected!")
# else:
#   print("I didn't get that.")
# import sys 

# user_args = sys.argv[1:]
# fun, games = user_args
# print(len(user_args))

fileN = fileName.split('/')[-1]

xml_extension_removed = re.sub('-urls.xml', '', str(fileN))

print(fileN)
print(xml_extension_removed)