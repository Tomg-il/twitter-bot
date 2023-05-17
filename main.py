""" this project checks my internet connection performance and post tweeter the result
if under the committed rate"""
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

COMMITTED_DOWN = 700
COMMITTED_UP = 100
TWITTER_USER = os.environ.get("TWITTER_USER")
TWITTER_PASS = os.environ.get("TWITTER_PASS")


class InternetSpeedTwitterBot:

    def __init__(self):
        self.up = 0
        self.down = 0

    def get_internet_seed(self):
        options = webdriver.ChromeOptions()
        options.add_argument('lang=en')
        speed_driver = webdriver.Chrome(options=options)
        speed_driver.get("https://www.speedtest.net/")

        go_button = speed_driver.find_element(by=By.LINK_TEXT, value="GO")
        go_button.click()
        sleep(40)
        self.up = \
            float(speed_driver.find_element(by=By.CLASS_NAME, value="download-speed").text)
        self.down = \
            float(speed_driver.find_element(by=By.CLASS_NAME, value="upload-speed").text)

    def tweet_at_provider(self):
        tweet_text = f"I am having low internet connection, last test showed {self.down}Mb/s " \
                     f"down and {self.up}Mb/s up ⚡\n"

        # # -- Login twitter     --- #
        options = webdriver.ChromeOptions()
        options.add_argument('lang=en')
        twitter_driver = webdriver.Chrome(options=options)

        twitter_driver.get("https://twitter.com/home")
        sleep(3)
        twitter_driver.find_element(by=By.NAME, value="text").send_keys(TWITTER_USER)
        sleep(3)
        next_button = twitter_driver.find_element(by=By.XPATH,
                                                  value='//span[text()="Next"]')

        sleep(3)
        next_button.click()
        sleep(5)

        twitter_driver.find_element(by=By.NAME, value="password").send_keys(TWITTER_PASS)
        sleep(5)
        login_button = twitter_driver.find_element(by=By.XPATH,
                                                   value='//span[text()="Log in"]')
        sleep(5)
        login_button.click()
        sleep(5)

    # -- send tweet on twitter ---- #
        sleep(5)
        tweet_input = twitter_driver.find_element(By.CSS_SELECTOR, "br[data-text='true']")
        sleep(3)
        tweet_input.send_keys(tweet_text)
        sleep(4)

        tweet_button = twitter_driver.find_element(By.CSS_SELECTOR,
                                                   'div[data-testid="tweetButtonInline"] div span')
        tweet_button.click()
        sleep (20)


# ------ check internet provider speed on speedtest.net-------#
speed_bot = InternetSpeedTwitterBot()
speed_bot.get_internet_seed()
print(speed_bot.up, speed_bot.down)

# --- if speed is lower than committed use the Twitter bot to tweet --- #
if speed_bot.down < COMMITTED_DOWN or speed_bot.up < COMMITTED_UP:
    speed_bot.tweet_at_provider()

