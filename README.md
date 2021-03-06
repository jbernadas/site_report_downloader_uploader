# Site Report with File Downloader and Uploader

A sitemapper, which maps all the internal pages of a website. It includes a downloader and uploader of all documents and images of a website.

## Installation

1. Clone to your computer.

   ```bash
   git clone git@github.com:jbernadas/site_report_downloader_uploader.git
   ```
2. Cd into the newly created directory.

3. Create a virtual environment inside the root directory.
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment.
    * Windows: 
      ```bash 
      venv\Scripts\activate
    * Linux/MacOS
      ```bash
      source venv\bin\activate
5. Install all requirements by issuing command: 
    ```bash
    pip install -r requirements.txt
    ```
On Windows you might run into an issue while installing Reppy, this is due to the missing Microsoft Build Tools. This is available through the below link: https://download.microsoft.com/download/5/F/7/5F7ACAEB-8363-451F-9425-68A90F98B238/visualcppbuildtools_full.exe

## How to use
The entry point is site_report.py so start it up by issuing command: 
  ```bash 
  python3 site_report.py
  ```
All output files will be in the site_report directory.
Thanks for looking!
