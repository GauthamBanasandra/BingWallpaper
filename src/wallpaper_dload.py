import re
import urllib

from selenium import webdriver


def get_filename(url):
    return url[url.rindex('/') + 1:]


def modify_dim(url, dim):
    return re.sub(r'_\d+x\d+\.jpg', '_' + dim + '.jpg', url)


download_path = r'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\wallpapers/'
phantom_js_path = r'C:\Users\Gautham B A\Documents\Projects\Github\BingWallpaper\deps\phantomjs.exe'
driver = webdriver.PhantomJS(executable_path=phantom_js_path)
driver.maximize_window()

# Open the webpage.
driver.get('http://www.bing.com/gallery/')
for i in range(1, 11):
    # Image on the page.
    div = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']')
    img = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']/img')
    if div is not None or img is not None:
        src = img.get_attribute('src')
        # Getting a bigger image.
        src = modify_dim(src, '1920x1200')
        # Open HTTP connection.
        img = urllib.urlopen(src)
        # Download the image only if it exists.
        if img.getcode() == 200:
            # Save the image.
            with open(download_path + get_filename(src), 'wb') as img_file:
                img_file.write(img.read())
                print 'downloaded', src
        img.close()
