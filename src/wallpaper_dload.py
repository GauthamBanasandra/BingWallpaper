from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
driver.get('http://www.bing.com/gallery/')
img=driver.find_element_by_xpath('//*[@id="grid"]/div[1]')
# dload=driver.find_element_by_xpath('//*[@id="detailInner"]/div/div[2]/div[2]/div/div[4]/a[2]')'
ActionChains(driver).click(img).perform()