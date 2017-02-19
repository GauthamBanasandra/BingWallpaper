import os

from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

# Path to chromedriver.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui

chromedriver_path = 'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\deps\chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver_path
driver = webdriver.Chrome(chromedriver_path)
driver.maximize_window()

# Open the webpage.
driver.get('http://www.bing.com/gallery/')
for i in range(1, 11):
    try:
        # Image on the page.
        img = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']')
        # Click the image.
        ActionChains(driver).click(img).perform()
        ui.WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="detailInner"]/div/div[2]/div[2]/div/div[4]/a[2]')))
        # Download button.
        dload_button = driver.find_element_by_xpath('//*[@id="detailInner"]/div/div[2]/div[2]/div/div[4]/a[2]')
        # Click the download button.
        ActionChains(driver).click(dload_button).perform()
        # Close button
        close_button = driver.find_element_by_xpath('//*[@id="detailInner"]/div/div[3]')
        # Click the close button.
        ActionChains(driver).click(close_button).perform()
    except TimeoutException:
        print 'error', img.get_attribute('src')
