from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from typing import Union
from time import sleep
from . import settings
import json


class InstagramOSINT:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=5)


    def __navigate_to_target(self, target: str=None) -> bool:
        self.driver.get(F"{settings.BASE_URL}/{target}")


    def __get_target_photo(self, save: bool=False) -> Union[str, None]:
        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'img[data-testid="user-avatar"]'))
        except exceptions.TimeoutException:
            return None
        else:
            photo = self.driver.find_element(By.CSS_SELECTOR, 'img[data-testid="user-avatar"]')
            return photo.get_attribute("src")


    def __get_target_name(self) -> Union[str, None]:
        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'span[class="_7UhW9    vy6Bb       qyrsm KV-D4            se6yk       T0kll "]'))
        except exceptions.TimeoutException:
            return None
        else:
            name = self.driver.find_element(By.CSS_SELECTOR, 'span[class="_7UhW9    vy6Bb       qyrsm KV-D4            se6yk       T0kll "]')
            return name.text


    def __is_target_private(self) -> bool:
        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'article[class="ySN3v"] > div > div > h2[class="rkEop"]'))
        except exceptions.TimeoutException:
            return False
        else:
            # private = self.driver.find_element(By.CSS_SELECTOR, 'article[class="ySN3v"] > div > div > h2[class="rkEop"]')
            return True

    
    def __is_target_verified(self) -> bool:
        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'span[title="Verified"]'))
        except exceptions.TimeoutException:
            return False
        else:
            # verified = self.driver.find_element(By.CSS_SELECTOR, 'span[title="Verified"]')
            return True


    def __get_target_category(self) -> Union[str, None]:
        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'div[class="_7UhW9    vy6Bb     MMzan    _0PwGv          uL8Hv        T0kll "]'))
        except exceptions.TimeoutException:
            return None
        else:
            category = self.driver.find_element(By.CSS_SELECTOR, 'div[class="_7UhW9    vy6Bb     MMzan    _0PwGv          uL8Hv        T0kll "]')
            return category.text


    def __get_target_posts(self) -> str:
        posts = ""

        if self.__is_target_private():
            posts = self.driver.find_element(By.CSS_SELECTOR, 'ul[class="k9GMp "] > li:nth-child(1)')
            posts = posts.find_element(By.CSS_SELECTOR, 'span[class="g47SY "]')
        else:
            posts = self.driver.find_element(By.CSS_SELECTOR, 'div[class="_7UhW9    vy6Bb     MMzan   KV-D4           uL8Hv        T0kll "] > span[class="g47SY "]')
        return posts.text


    def __get_target_followers(self, target: str=None) -> str:
        followers = ""

        if self.__is_target_private():
            followers = self.driver.find_element(By.CSS_SELECTOR, 'ul[class="k9GMp "] > li:nth-child(2)')
            followers = followers.find_element(By.CSS_SELECTOR, 'span[class="g47SY "]')
        else:
            followers = self.driver.find_element(By.CSS_SELECTOR, F'a[href="/{target}/followers/"] > div > span[class="g47SY "]')
        return followers.get_attribute("title")


    def __get_target_following(self, target: str=None) -> Union[str, None]:
        following = ""

        if self.__is_target_private():
            following = self.driver.find_element(By.CSS_SELECTOR, 'ul[class="k9GMp "] > li:nth-of-type(3)')
            following = following.find_element(By.CSS_SELECTOR, 'span[class="g47SY "]')
        else:
            following = self.driver.find_element(By.CSS_SELECTOR, F'a[href="/{target}/following/"] > div > span[class="g47SY "]')
        return following.text
        

    def __get_target_website(self) -> Union[str, None]:
        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'a[rel="me nofollow noopener noreferrer"]'))
        except exceptions.TimeoutException:
            return None
        else:
            website = self.driver.find_element(By.CSS_SELECTOR, 'a[rel="me nofollow noopener noreferrer"]')
            return website.text


    def get_target_info(self, target: str=None, save: bool=False) -> str:
        self.__navigate_to_target(target)
        sleep(2)

        target_data: list = {
            "username": target,
            "name": self.__get_target_name(),
            "photo_link": self.__get_target_photo(),
            "posts": self.__get_target_posts(),
            "followers": self.__get_target_followers(target),
            "following": self.__get_target_following(target),
            "category": self.__get_target_category(),
            "website": self.__get_target_website(),
            "private": self.__is_target_private(),
            "verified": self.__is_target_verified(),
        }

        if save:
            json.dump(target_data, open(F"userdata/backupcode/{settings.LOGIN['username']}.json", "w"))

        return target_data
        

