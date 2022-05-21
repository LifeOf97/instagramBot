from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from pathlib import Path
from time import sleep
import json

# Dynamic path
BASE_DIR = Path(__file__).parent


class InstagramLogin:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)


    def __input_username(self, username):
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)


    def __input_password(self, password):
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)


    def __input_username_password(self, username: str=None, password: str=None) -> None:
        try: # check that login button loaded
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))
        except exceptions.TimeoutException:
            print("Timeout: username and password")
        else:
            self.__input_username(username)
            self.__input_password(password)
            sleep(1)


    def __save_cookies(self, username: str=None) -> None:
        cookies = self.driver.get_cookies()
        json.dump(cookies, open(F"{BASE_DIR}/userdata/cookies/{username}.json", "w"))


    def __turn_on_notifications(self, turn_on=False) -> None:
        if turn_on:
            try:
                self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'button[class="aOOlW  bIiDR  "]'))
            except exceptions.TimeoutException:
                print(F"[!] Timeout: turn on notification")
            else:
                self.driver.find_element(By.CSS_SELECTOR, 'button[class="aOOlW  bIiDR  "]').click()
                print(F"[x] Notifications turned on")
        else:
            try:
                self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'button[class="aOOlW   HoLwm "]'))
            except exceptions.TimeoutException:
                print(F"[!] Timeout: turn off notification")
            else:
                self.driver.find_element(By.CSS_SELECTOR, 'button[class="aOOlW   HoLwm "]').click()
                print(F"[x] Notifications turned off")
    

    def __save_login_info(self, username: str=None, save_login: bool=True) -> None:
        if save_login:
            try:
                self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'button[class="sqdOP  L3NKy   y3zKF     "]'))
            except exceptions.TimeoutException:
                print(F"[!] Timeout: save login")
            else:
                self.driver.find_element(By.CSS_SELECTOR, 'button[class="sqdOP  L3NKy   y3zKF     "]').click()
                self.__save_cookies(username)
                print(F"[x] Login saved")
                self.__turn_on_notifications(turn_on=False)
        else:
            try:
                self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'button[class="sqdOP yWX7d    y3zKF     "]'))
            except exceptions.TimeoutException:
                print(F"[!] Timeout: don't save login")
            else:
                self.driver.find_element(By.CSS_SELECTOR, 'button[class="sqdOP yWX7d    y3zKF     "]').click()
                print(F"[x] Login not saved")
                self.__turn_on_notifications(turn_on=False)


    def __input_otp(self, username: str=None, otp: str=None) -> bool:
        self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]'))
        sleep(1)

        otp_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]')
        otp_decription = self.driver.find_element(By.ID, 'verificationCodeDescription').text
        otp_field.send_keys(input(F"[+] {otp_decription}: "))

        self.driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()

        try: # is user redirected to the save info url.
            self.wait.until(expected_conditions.url_contains(r"accounts/onetap/?next=%2F"))
        except exceptions.TimeoutException: # clear the input field and output the error message
            otp_field.send_keys(Keys.CONTROL, "a")
            otp_field.send_keys(Keys.DELETE)

            error_message = self.driver.find_element(By.ID, "twoFactorErrorAlert").text
            print(F"Error: {error_message}")
            return False
        else:
            print("[x] Logged in via username/password and 2FA")
            self.__save_login_info(username)
            return True

    
    def login_via_cookies(self, username: str=None) -> bool:
        """
        This methods populates the cookies field of this web instance with the cookies
        saved from the last time you logged into instagram if you had set save_login
        to true on the login_via_login method.
        """
        try:
            for cookie in json.load(open(F"{BASE_DIR}/userdata/cookies/{username}.json", "r")):
                self.driver.add_cookie(cookie)
        except Exception as e: # no cookies available
            return False
        else:
            self.driver.refresh()
            
            try: # is the turn on notification modal present?
                self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'div[class="mt3GC"] > button[class="aOOlW   HoLwm "]'))
            except exceptions.TimeoutException:
                return False
            else:
                print("[x] Logged in via cookies")
                self.__turn_on_notifications(turn_on=False)
                return True
        

    def login_via_login(self, username: str=None, password: str=None, save_login: bool=True) -> list:
        """
        Log in to istagram with the provided credentials.

        username: account username, email or phone number. Required
        password: account password. Required
        save_login: should your login cookies be saved. Optional
        default is True.

        Returns a list
        [0, "error_msg"]: means user could not log in.
        [1, "logged in"]: means user logged in successfully [without 2FA] 
        return value None: means 2FA otp is required [needs otp] 
        """
        self.__input_username_password(username, password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        try: # check for 2FA
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'input[name="verificationCode"]'))
        except exceptions.TimeoutException:

            # no 2FA
            if r"accounts/onetap/?next=%2F" in self.driver.current_url:
                print("[x] Logged in via username/password")
                self.__save_login_info(username, save_login)
                return [1, "logged in"]
            else:
                error_message = self.driver.find_element(By.ID, "slfErrorAlert").text
                print(F"[!] Error: {error_message}")
                self.driver.quit()
                return [0, error_message]

        else:
            print("[x] 2FA is enabled")

            while True:
                otp = self.__input_otp(username=username)
                
                if otp:
                    break