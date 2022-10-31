from selenium import webdriver

import time

# 设置手机访问
mobileEmulation = {"deviceName": "iPhone 6"}
# 设置 Chorme
chromeOptions = webdriver.ChromeOptions()
# 禁用日志打印
chromeOptions.add_experimental_option(
    'excludeSwitches', ['enable-logging']
)
chromeOptions.add_experimental_option(
    'mobileEmulation', mobileEmulation
)

driver = webdriver.Chrome(
    executable_path=r'E:\Driver\chromedriver.exe', options=chromeOptions)

url = 'https://y.music.163.com/m/playlist?id=90771773'
driver.get(url)

time.sleep(60)

text = driver.get_cookies()

print(text)
driver.quit()