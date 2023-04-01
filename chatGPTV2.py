import os
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()

settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": ""
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "isLandscapeEnabled": True,
    "isCssBackgroundEnabled": True,
    "mediaSize": {
        "height_microns": 297000,
        "name": "ISO_A4",
        "width_microns": 210000,
        "custom_display_name": "A4 210 x 297 mm"
    },
}

savepath = r"D:\static\pdf"
if not os.path.exists(savepath):
    os.makedirs(savepath)

prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    'savefile.default_directory': savepath
}

chrome_options.add_argument('--enable-print-browser')
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome()

for filename in os.listdir(r"D:\static"):
    if filename.endswith(".html"):
        filepath = os.path.join(r"D:\static", filename)
        driver.get(f'file:///{filepath}')
        driver.maximize_window()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        driver.execute_script('document.title="test.pdf";window.print();')
        WebDriverWait(driver, 60).until(lambda driver: len(os.listdir(savepath)) > 0)
        time.sleep(2)  # wait for the file to be fully written to disk
driver.quit()