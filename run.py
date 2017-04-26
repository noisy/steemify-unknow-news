import sys
import os
import time
import validators
import datetime

from selenium import webdriver

###################################
# IMAGE HOSTING SERVER SETTINGS
IMG_HOST_BASE_DIR = '/var/www/images/'
TARGET_LINK_PATTERN = 'http://myserver/images/{dir}/{file}'
USER = ''
HOST = ''
IDENTIFY_FILE = '/home/myname/.ssh/id_rsa'


# SELENIUM
CHROME_DRIVER_PATH = '/home/myname/chromedriver'
###################################


def get_selenium_driver():
    os.environ["webdriver.chrome.driver"] = CHROME_DRIVER_PATH
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.set_window_size(1280, 960)

    return driver


def scpr(src, dst):
    cmd = 'scp -r -i {identifyfile} {src} {user}@{host}:{dst}'.format(
        identifyfile=IDENTIFY_FILE,
        src=src,
        user=USER,
        host=HOST,
        dst=dst
    )
    os.system(cmd)


def main():

    driver = get_selenium_driver()

    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    os.system('mkdir -p img/' + date_str)

    i = 1
    for line in sys.stdin.readlines():
        print(line)
        line = line.strip()

        if validators.url(line) and not (line.endswith('png') or line.endswith('jpg')):

            driver.get(line)
            time.sleep(5)
            screenshot = '{}.png'.format(i)
            driver.save_screenshot(os.path.join('img', date_str, screenshot))
            print(TARGET_LINK_PATTERN.format(dir=date_str, file=screenshot))

            i += 1

    src = os.path.join('img', date_str)
    dst = os.path.join(IMG_HOST_BASE_DIR, date_str)

    scpr(src, dst)

if __name__ == '__main__':
    if os.isatty(0):
        print('usage: cat unknownews.txt | python run.py')
    else:
        main()
