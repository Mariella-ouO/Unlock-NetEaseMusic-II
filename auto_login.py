# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00FF7422C9B3E56E4308B7F755AE0B7F550C16336E6FB14B5DAD13E64EBEF77B675A73BEA2372225DFE2CB27069F708A8977CE683C7B1B885892A79A134AA647A3B6162B026F968B3F043A56F4EB094970B9B4354F34453FF9A80E38D23D04DA48189370EC9A8418250F2FA4E95CF781C2E1C7C10D602FE8451E6B683C19E94922DF747BD9189A6207584F244F7D6BB78B0061B20B9AE5FFF154962A90AEEE07786E2A97AA084670E9499B46ADEC6B15EC4FA4FD7494B8394CCBF81673C50CBBCBB651FA2F005A904BB43F2590F139F27695EB5A4418960F2310197C3CC5F6EE1B4E10B01307A40818CBF858E71A37C9EBC8EC7B28128408455BF90EB93C26E8E80083F99DFC71BBD10555530D47020EBD944CE0EE9AE34E97A716F5B3FED19DFAF048A36733BCE9519D8FBD86DAB4B124C8BF037509482B29DE901B51E3E678737BBD39A555CA239A4E5956E0C701728EB5F1761EA87DC5643FFBB146C2A4C6F4"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")
    
    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
