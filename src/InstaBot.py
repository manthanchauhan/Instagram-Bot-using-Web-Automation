"""
class definition of InstaBot
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import *


class InstaBot:
    def __init__(self, email, password, username):
        self.browser = webdriver.Chrome('/home/manthan/bots/instabot/chromedriver')
        self.email = email
        self.password = password
        self.username = username

    def __enter__(self):
        self.sign_in()
        return self

    def sign_in(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        email_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'username')))

        password_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        # confirms login by searching for Instagram logo
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/span'))
        )

    def follow_with_username(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')

        try:
            follow_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Follow"]')))
        except TimeoutException:
            # already following
            return False

        follow_button.click()
        return True

    def unfollow_with_username(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(3)

        try:
            follow_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "yZn4P"))
            )
        except TimeoutException:
            # might be in "Requested" state
            try:
                follow_button = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_8A5w5"))
                )
            except TimeoutException:
                # not following
                return

        follow_button.click()

        confirm_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Unfollow"]'))
        )
        confirm_button.click()

    def get_user_followers(self, username, nums: int = -1):
        self.browser.get('https://www.instagram.com/' + username)

        if nums == -1:
            # get total number of followers
            nums = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, 'g47SY')))[1]
            nums = int(nums.text)

        # open followers list
        followers_link = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, '-nal3')))[1]
        followers_link.click()

        try:
            followers_list = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((
                By.CLASS_NAME, '_6xe7A')))
        except TimeoutException:
            # 0 followers
            return []

        num = len(followers_list.find_elements_by_css_selector('li'))

        followers_list.click()
        action_chain = webdriver.ActionChains(self.browser)

        while num < nums:
            followers_list.click()
            action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            num = len(followers_list.find_elements_by_css_selector('li'))
            # print(num)

        followers_list = followers_list.find_elements_by_css_selector('li')[0:nums]

        followers = [user.find_elements_by_css_selector('a')[-1].text
                     for user in followers_list]

        return followers

    def __exit__(self, exception_type, exception_value, traceback):
        self.browser.quit()

    def inc_followers(self, host_username: str = 'manthan913',
                      prim_followers: int = -1,
                      secon_followers: int = -1,
                      ):
        result = self.follow_with_username(host_username)
        if result:
            return 1

        stage1_followers = self.get_user_followers(username=host_username,
                                                   nums=prim_followers,
                                                   )

        count = 0

        for follower in stage1_followers:
            if follower == self.username:
                continue

            result = self.follow_with_username(follower)
            count += int(result)

            if result:
                continue

            stage2_followers = self.get_user_followers(username=follower,
                                                       nums=secon_followers,
                                                       )
            for follower_ in stage2_followers:
                result = self.follow_with_username(follower_)
                count += int(result)
        return count


