import os
import json
import time
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, as_completed

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
# 静默打印，无需用户点击打印页面的确定按钮
chrome_options.add_argument('--kiosk-printing')

# 不弹窗
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')


chrome_options.add_experimental_option('prefs', prefs)

# 定义处理单个文件的函数
def process_file(file_path):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'file:///{file_path}')
    time.sleep(10)
    driver.execute_script('window.print();')
    driver.execute_script('window.close();')
    driver.quit()

# 初始化线程池
executor = ThreadPoolExecutor(max_workers=5)

# 列出所有HTML文件并逐个加入到线程池中处理
html_folder_path = r'D:\0_ycy_code\rongketong\rkt-evaluation\evaluation-boot\src\main\resources\static'
future_to_file = {}
for file_name in os.listdir(html_folder_path):
    if file_name.endswith('.html'):
        file_path = os.path.join(html_folder_path, file_name)
        future = executor.submit(process_file, file_path)
        future_to_file[future] = file_path

# 等待所有任务完成并输出结果
for future in as_completed(future_to_file):
    file_path = future_to_file[future]
    try:
        result = future.result()
    except Exception as exc:
        print('%r generated an exception: %s' % (file_path, exc))
    else:
        print('%r completed successfully' % file_path)