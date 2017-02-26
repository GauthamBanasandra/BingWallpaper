import os
import urllib

from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui


# # Path to chromedriver.
# chromedriver_path = 'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\deps\chromedriver.exe'
# # Set the download path (May not be necessary).
# chrome_options = webdriver.ChromeOptions()
# preferences = {'download.default_directory': 'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\wallpapers'}
# chrome_options.add_experimental_option('prefs', preferences)
#
# # Chrome web driver.
# driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
def get_filename(url):
    return url[url.rindex('/') + 1:]


download_path = r'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\wallpapers/'
phantom_js_path = r'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\deps\phantomjs.exe'
driver = webdriver.PhantomJS(executable_path=phantom_js_path)
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
            # Getting a bigger image.
            src = src.replace('320x180', '1920x1200')
            # Download the image through HTTP.
            with open(download_path + get_filename(src), 'wb') as img_file:
                img = urllib.urlopen(src).read()
                img_file.write(img)
            print 'downloaded', src
    except TimeoutException:
        print 'unavailable for download', src
