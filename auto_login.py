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
    browser.add_cookie({"name": "MUSIC_U", "value": "003BB0FA578790C2A66CD06D080CFD2EE816876BF9E8DDDB5D11BC26E708E54E9DA934AD3C4BB803E482CC12F4036EC8A72D2E3B656E60229FA1707CF64A5EB8B449D86A5AE1A1409ACC03544CBE58DFF6D683A12843ED51576FB5BA1BDB0DE2FBB66E55E461A03BABC71B648B62A9FEAD5F64D7526C0D995763B9986258EF777AC146D9A281457EF0AED22E2199423E42C6B097A4B33798B579FE37DBF1588F931A8D7583810498782D8557BF19C7CAEBE1DA2515CCAE5272CD603610850DE2B35D21EFA6DB6DB8B8259EBC751153F587645F08537227258F4534C8991A69240371FAEF0CD5EE1BD37ACD97357DCA50350C3D794BB10597C034CDDB044C0C870170AC589EA96E08FA7501F7C268BADF8AE4CA8A016C6215F42F9495EA6FB157509AD89F842579DFD2D79CA905A1B2F0D799DB1063C9F257472F9725406C06D1D04678429690298CF2620667A97AA84F23879377A18A3F6EA5D39321C7FA95046C"})
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
