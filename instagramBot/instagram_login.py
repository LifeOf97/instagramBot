from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from instagramBot import settings
from time import sleep
import json


class InstagramLogin:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)


    def __input_username_password(self, username: str=None, password: str=None) -> None:
        try: # wait for the login button
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))
        except exceptions.TimeoutException:
            print("Timeout: username and password")
        else:
            self.driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)
            self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)


    def __input_twofa_otp(self, otp: str=None) -> bool:
        self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]'))
        sleep(1)

        otp_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]')
        otp_decription = self.driver.find_element(By.ID, 'verificationCodeDescription').text
        otp_field.send_keys(input(F"[+] {otp_decription}: "))

        self.driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()

        try: # user is redirected to the save info modal url.
            self.wait.until(expected_conditions.url_contains(r"accounts/onetap/?next=%2F"))
        except exceptions.TimeoutException:
            otp_field.send_keys(Keys.CONTROL, "a")
            otp_field.send_keys(Keys.DELETE)

            error_message = self.driver.find_element(By.ID, "twoFactorErrorAlert").text
            print(F"Error: {error_message}")
            return False
        else:
            return True


    def __save_login_info(self, save_login=False) -> None:
        if save_login:
            self.driver.find_element(By.CSS_SELECTOR, 'div[class="JErX0"] > .L3NKy').click()
            self.__save_cookies()
            print(F"[x] Login saved")
            sleep(2)
            self.__turn_on_notifications(turn_on=False)
        else:
            self.driver.find_element(By.CSS_SELECTOR, 'div[class="cmbtv"] > .yWX7d').click()
            print(F"[x] Login not saved")
            sleep(2)
            self.__turn_on_notifications(turn_on=False)


    def __save_cookies(self) -> None:
        cookies = self.driver.get_cookies()
        json.dump(cookies, open(F"userdata/cookies/{settings.LOGIN['username']}.json", "w"))
    

    def __turn_on_notifications(self, turn_on=False) -> None:
        if turn_on:
            self.driver.find_element(By.CSS_SELECTOR, 'div[class="mt3GC"] > button[class="aOOlW  bIiDR  "]')
            print(F"[x] Notifications turned on")
        else:
            self.driver.find_element(By.CSS_SELECTOR, 'div[class="mt3GC"] > button[class="aOOlW   HoLwm "]').click()
            print(F"[x] Notifications turned off")

    
    def login_via_cookies(self) -> bool:
        """
        This methods populates the cookies field of this web instance with the cookies
        saved from the last time you logged into instagram if you had set save_login
        to true on the login_via_login method.
        """
        try:
            for cookie in json.load(open(F"userdata/cookies/{settings.LOGIN['username']}.json", "r")):
                self.driver.add_cookie(cookie)
        except Exception as e: # no cookies available
            return False
        else:
            self.driver.refresh()
            
            try: # is the turn on notification modal present?
                self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'div[class="mt3GC"] > button[class="aOOlW   HoLwm "]'))
            except exceptions.TimeoutException:
                # print("[x] Logged in via cookies")
                return False
            else:
                print("[x] Logged in via cookies")
                self.__turn_on_notifications(turn_on=False)
                return True
        

    def login_via_login(self, username: str=None, password: str=None, save_login: bool=True) -> None:
        """
        Log in to istagram with the provided credentials.

        username: account username, email or phone number. Required
        password: account password. Required
        save_login: should your login cookies be saved. Optional
        default is True.
        """
        self.__input_username_password(username, password)
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        try: # check for 2FA
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]'))
        except exceptions.TimeoutException:
            print("[x] 2FA is not enabled")
        else:
            print("[x] 2FA is enabled")

            while True:
                otp = self.__input_twofa_otp()
                
                if otp:
                    break
        
                # self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]'))
                # sleep(1)

                # otp_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]')
                # otp_decription = self.driver.find_element(By.ID, 'verificationCodeDescription').text
                # otp_field.send_keys(input(F"{otp_decription}: "))
                # self.driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()

                # try: # user is redirected and the save info modal is present
                #     self.wait.until(expected_conditions.url_contains(r"accounts/onetap/?next=%2F"))
                # except exceptions.TimeoutException:
                #     # clear otp field
                #     otp_field.send_keys(Keys.CONTROL, "a")
                #     otp_field.send_keys(Keys.DELETE)

                #     error_message = self.driver.find_element(By.ID, "twoFactorErrorAlert").text
                #     print(F"Error: {error_message}")
                # else:
                #     break
    
        try: # if no 2FA, check for save login info modal
            self.wait.until(expected_conditions.url_contains(r"accounts/onetap/?next=%2F"))
        except exceptions.TimeoutException:
            error_message = self.driver.find_element(By.ID, "slfErrorAlert").text
            print(F"Error: {error_message}")
        else:
            print("[x] Logged in via username/password")
            self.__save_login_info(save_login)