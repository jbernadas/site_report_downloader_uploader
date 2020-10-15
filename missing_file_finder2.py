import os

list_file = open('./site_report/ldrd-annual-prod/imgs-ldrd-annual-prod.txt', 'r')

prodsite_imgs = list_file.read().split(',')

list_file.close()

origsite_imgs = os.listdir('./site_report/ldrd-annual/imgs_for_upload/')

count = 0

for img in prodsite_imgs:
  if img not in origsite_imgs:
    print(img)
  else:
    continue

print("There are {} images not in prod site.".format(count))

