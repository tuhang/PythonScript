import os
import json
import time
from selenium import webdriver


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

# 设置下载文件夹路径
download_folder_path = r'd:\static\pdf'
prefs = {
    'download.default_directory': download_folder_path,
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
}

chrome_options.add_argument('--enable-print-browser')
#静默打印，无需用户点击打印页面的确定按钮
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_experimental_option('prefs', prefs)

# 初始化浏览器
driver = webdriver.Chrome(options=chrome_options)

# 列出所有HTML文件并逐个打开
html_folder_path = r'd:\static'
for file_name in os.listdir(html_folder_path):
    if file_name.endswith('.html'):
        file_path = os.path.join(html_folder_path, file_name)
        driver.get(f'file:///{file_path}')

        # 等待页面加载完成
        driver.execute_script('window.print();')
        time.sleep(60)
        driver.execute_script('window.close();')

# 关闭浏览器
driver.quit();




