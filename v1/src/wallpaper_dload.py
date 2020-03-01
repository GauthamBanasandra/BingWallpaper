import json
import os
import re
import urllib

import sys
from selenium import webdriver


# Returns the file name from the url.
def get_filename(url):
    return url[url.rindex('/') + 1:]


# Modifies the dimension of the image in the url.
def modify_dim(url, dim):
    return re.sub(r'_\d+x\d+\.jpg', '_' + dim + '.jpg', url)


# Checks if the image is already saved.
def is_saved(url):
    return get_filename(url) in saved_imgs


# Path of the config file.
config_path = sys.argv[1]
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# Append a '/' to the download path, if necessary.
if config['download_path'][-1] == '/' or config['download_path'][-1] == '\\':
    download_path = config['download_path']
else:
    download_path = config['download_path'] + '/'

# Image count - number of images that will be downloaded in the current run.
img_count = config['image_count']
# Gets a set of the saved images.
saved_imgs = set(os.listdir(download_path))
driver = webdriver.PhantomJS()
driver.maximize_window()

# Open the webpage.
driver.get('http://www.bing.com/gallery/')

i = 0
while img_count:
    i += 1
    # Image on the page.
    div = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']')
    img = driver.find_element_by_xpath('//*[@id="grid"]/div[' + str(i) + ']/img')
    if div is not None or img is not None:
        src = img.get_attribute('src')
        # Getting a bigger image.
        src = modify_dim(src, '1920x1200')
        if not is_saved(src):
            # Open HTTP connection.
            img = urllib.urlopen(src)
            # Download the image only if it exists.
            if img.getcode() == 200:
                # Save the image.
                with open(download_path + get_filename(src), 'wb') as img_file:
                    img_file.write(img.read())
                    print 'downloaded', src
                img_count -= 1
            img.close()
