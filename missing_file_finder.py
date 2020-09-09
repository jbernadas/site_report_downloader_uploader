
## This script compares two directories and tells you
## which files are found on the ORIGINAL site but not
## found on the PROD site. It bases it's finding

import filecmp

orig = 'site_report/wci/imgs_for_upload'
prod = 'site_report/wci-prod/imgs_for_upload'

c = filecmp.dircmp(orig, prod)

def report_recursive(dcmp):
  orig_count = 0
  # Count all missing files from PROD site
  for name in dcmp.left_only:
    print("%s was NOT found in PROD" % (name))
    orig_count += 1
        
  print("There are %s files NOT found in PROD" % (orig_count))
  print("Preparing file uploader to upload missing files.")
  ## Fire-up our uploader script


  ## Recursively upload missing files to PROD site
  # for name in dcmp.left_only:

report_recursive(c)
