import os

from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui

# Path to chromedriver.
chromedriver_path = 'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\deps\chromedriver.exe'
# Set the download path (May not be necessary).
chrome_options = webdriver.ChromeOptions()
preferences = {'download.default_directory': 'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\wallpapers'}
chrome_options.add_experimental_option('prefs', preferences)

# Chrome web driver.
driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
driver.maximize_window()

# Open the webpage.
driver.get('http://www.bing.com/gallery/')
for i in range(1, 11):
    try:
        # Image on the page.
        div = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']')
        img = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']/img')
        if div is not None or img is not None:
            src = img.get_attribute('src')
            # Click the image.
            ActionChains(driver).click(img).perform()
            ui.WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="detailInner"]/div/div[2]/div[2]/div/div[4]/a[2]')))
            # Download button.
            dload_button = driver.find_element_by_xpath('//*[@id="detailInner"]/div/div[2]/div[2]/div/div[4]/a[2]')
            # Click the download button.
            ActionChains(driver).click(dload_button).perform()
            print 'downloaded', src
    except TimeoutException:
        print 'unavailable for download', src
    except StaleElementReferenceException:
        print 'no download button'
    finally:
        if div is not None:
            div.send_keys(Keys.ESCAPE)
