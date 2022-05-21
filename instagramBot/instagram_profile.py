from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from pathlib import Path
from . import settings
from time import sleep


# Dynamic path
BASE_DIR = Path(__file__).parent

class InstagramProfile:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)

    
    def __navigate_to_account_edit(self):
        self.driver.get(settings.ACCOUNT_EDIT_URL)

    
    def __navigate_to_change_password(self):
        self.driver.get(settings.CHANGE_PASSWORD_URL)

    
    def __navigate_to_twofa(self):
        self.driver.get(settings.TWOFA_URL)

    
    def __input_otp(self, otp: str=None) -> bool:
        code_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="confirmationCode"]')
        done_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[class="sqdOP  L3NKy   y3zKF     "]')
        
        code_field.send_keys(input("[+] Confirmation code: "))
        sleep(1)
        done_btn.click()

        try: # wait for bottom notification bar to show up
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'div[class="ToanC XjicZ"]'))
        except exceptions.TimeoutException:
            code_field.clear()
            print("[!] Timeout: enable twofa > verify code")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'div[class="ToanC XjicZ"]')

            if "settings saved" in str(bottom_notif.text.lower()):
                print(F"[x] {bottom_notif.text}")
                return True
            else:
                code_field.clear()
                print(bottom_notif.text)
                return False


    def update_profile_email(self, email: str=None) -> bool:
        """
        email: email to provide to instagram. Required

        NOTE: You will be sent an email to verify this email address by logging into the site,
        so you'll need the account username/password and 2FA if enabled.
        """
        self.__navigate_to_account_edit()
        sleep(1)

        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pepEmail"]')
        email_field.clear()
        email_field.send_keys(email)

        # click submit button
        self.driver.find_element(By.CLASS_NAME, "L3NKy").click()

        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Update email")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]')

            if "profile saved" in str(bottom_notif.text.lower()):
                print("[x] Email updated successfully")
                return True
            else:
                print(F"Error: {bottom_notif.text}")
                return False


    def update_profile_phone(self, phone: str=None) -> bool:
        """
        phone: phone to provide to instagram. Required
        should include country call code.
        Syntax: +2341234567890.

        NOTE: phone number can only be changed if 2FA is disabled. You need to disable 2FA
        first before updating phone number or you update the 2FA phone that recieves the OTP directly.
        """
        self.__navigate_to_account_edit()
        sleep(1)

        phone_field = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pepPhone Number"]')
        phone_field.clear()
        phone_field.send_keys(phone)

        # click submit button
        self.driver.find_element(By.CLASS_NAME, "L3NKy").click()

        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Update phone")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]')

            if "profile saved" in str(bottom_notif.text.lower()):
                print("[x] Phone updated successfully")
                return True
            else:
                print(F"[!] Error: {bottom_notif.text}")
                return False


    def update_profile_username(self, username: str=None) -> bool:
        """
        username: a unique username. Required

        NOTE: The username should be one that no other instagram account is currently using.
        """
        self.__navigate_to_account_edit()
        sleep(2)

        username_field = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pepUsername"]')
        username_field.clear()
        username_field.send_keys(username)

        # click submit button
        self.driver.find_element(By.CLASS_NAME, "L3NKy").click()

        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Update username")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]')

            if "profile saved" in str(bottom_notif.text.lower()):
                print("[x] Username updated successfully")
                return True
            else:
                print(F"[!] Error: {bottom_notif.text}")
                return False


    def update_profile_name(self, name: str=None) -> bool:
        """
        name: account name. Required

        NOTE: Instagram only allows your account name to be changed twice within 14 day.
        """
        self.__navigate_to_account_edit()
        sleep(2)

        name_field = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pepName"]')
        name_field.clear()
        name_field.send_keys(name)

        # click submit button
        self.driver.find_element(By.CLASS_NAME, "L3NKy").click()

        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Update name")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]')

            if "profile saved" in str(bottom_notif.text.lower()):
                print("[x] name updated successfully")
                return True
            else:
                print(F"[!] Error: {bottom_notif.text}")
                return False


    def update_profile_website(self, website: str=None) -> bool:
        """"
        website: website to add to your account. Required
        """
        self.__navigate_to_account_edit()
        sleep(2)

        website_field = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pepWebsite"]')
        website_field.clear()
        website_field.send_keys(website)

        # click submit button
        self.driver.find_element(By.CLASS_NAME, "L3NKy").click()

        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Update website")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]')

            if "profile saved" in str(bottom_notif.text.lower()):
                print("[x] Website updated successfully")
                return True
            else:
                print(F"[!] Error: {bottom_notif.text}")
                return False


    def update_profile_bio(self, bio: str=None) -> bool:
        """
        bio: About your self. Required
        """
        self.__navigate_to_account_edit()
        sleep(2)

        bio_field = self.driver.find_element(By.CSS_SELECTOR, 'input[id="pepBio"]')
        bio_field.clear()
        bio_field.send_keys(bio)

        # click submit button
        self.driver.find_element(By.CLASS_NAME, "L3NKy").click()

        try:
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Update bio")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]')

            if "profile saved" in str(bottom_notif.text.lower()):
                print("[x] Bio updated successfully")
                return True
            else:
                print(F"[!] Error: {bottom_notif.text}")
                return False


    def change_password(self, old_password: str=None, new_password: str=None, confirm_password: str=None) -> bool:
        """
        old_password: your account old passwrod. Required
        new_password: new passwrod. Required
        confiem_password: confirm new passwrod. Required
        """
        self.__navigate_to_change_password()
        sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, 'input[id="cppOldPassword"]').send_keys(old_password)
        self.driver.find_element(By.CSS_SELECTOR, 'input[id="cppNewPassword"]').send_keys(new_password)
        self.driver.find_element(By.CSS_SELECTOR, 'input[id="cppConfirmPassword"]').send_keys(confirm_password)

        self.driver.find_element(By.CSS_SELECTOR, 'button[class="sqdOP  L3NKy   y3zKF     "]').click()

        try:  # wait for bottom notification bar to show up
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: change password")
            return False
        else:
            bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"')

            if "password changed" in str(bottom_notif.text.lower()):
                print("[x] Password changed successfully")
                return True
            else:
                print(F"[!] Error: {bottom_notif.text}")
                return False

    
    def disable_twofa(self):
        """
        This method disables all two factor authentication method set on the account.
        Takes no arguments for now.
        """
        self.__navigate_to_twofa()

        try:
            self.wait.until(lambda elem: elem.find_elements(By.CSS_SELECTOR, 'input[class="tlZCJ"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: Disable 2fa")
        else:
            twofa_elems = self.driver.find_elements(By.CSS_SELECTOR, 'input[class="tlZCJ"]')

            for twofa in twofa_elems:
                if twofa.is_selected():
                    label_elem = self.driver.find_element(By.CSS_SELECTOR, F'label[for="{twofa.get_attribute("id")}"]')
                    label_elem.click()
                    sleep(1)

                    # click turn off button
                    self.driver.find_element(By.CSS_SELECTOR, 'button[class="aOOlW  bIiDR  "]').click()

                    try:  # wait for bottom notification bar to show up
                        self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"]'))
                    except exceptions.TimeoutException:
                        print("[!] Timeout: Disable 2fa > turn off")
                    else:
                        bottom_notif = self.driver.find_element(By.CSS_SELECTOR, 'p[class="gxNyb"')

                        if "settings saved" in str(bottom_notif.text.lower()):
                            print(F"[2FA] {label_elem.text} Turned off")
                            return True
                        else:
                            print(F"[2FA]: {label_elem.text}: Error")
                            return False


    def enable_sms_twofa(self, phone: str=None) -> None:
        """
        phone: provide the phone number to recieve otp. Required

        should include country call code.
        Syntax: +2341234567890.
        """
        self.__navigate_to_twofa()

        try:    
            self.wait.until(lambda elem: elem.find_elements(By.CSS_SELECTOR, 'input[class="tlZCJ"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: enable twofa")
        else:
            sms_twofa_label = self.driver.find_element(By.CSS_SELECTOR, 'label[class="U17kh PLphk "]')
            sms_twofa_checkbox = self.driver.find_element(By.CSS_SELECTOR, F'input[id="{sms_twofa_label.get_attribute("for")}"]')

            if not sms_twofa_checkbox.is_selected():
                sms_twofa_label.click()
                sleep(2)

                self.driver.find_element(By.CSS_SELECTOR, 'button[class="aOOlW  bIiDR  "]').click()
                phone_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="phoneNumber"]')
                next_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[class="sqdOP  L3NKy   y3zKF     "]')

                phone_field.clear()
                phone_field.send_keys(phone)
                next_btn.click()

                try:
                    self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'input[name="confirmationCode"]'))
                except exceptions.TimeoutException:
                    print("[!] Timeout: enable twofa > code input")
                else:
                    while True:
                        otp = self.__input_otp()

                        if otp:
                            break
           
            else:
                raise Exception("Text message twofa already enabled")

    
    def get_backup_code(self, username) -> bool:
        """
        This method saves the backup code for your account,
        It's only available when two factor authentication is set.

        username: account username. Required
        """
        self.__navigate_to_twofa()
        sleep(2)

        button_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[class="sqdOP yWX7d    y3zKF     "]')
        button_elem.click()

        try: # is backup code visible
            self.wait.until(lambda elem: elem.find_element(By.CSS_SELECTOR, 'article[class="PVkFi"] > div[class="_8hLoy"] > ul[class="U3GhF"]'))
        except exceptions.TimeoutException:
            print("[!] Timeout: get backup code > code")
        else:
            sleep(2)
            code_elem = self.driver.find_element(By.CSS_SELECTOR, 'article[class="PVkFi"] > div[class="_8hLoy"] > ul[class="U3GhF"]')
            code_lists = code_elem.find_elements(By.TAG_NAME, 'li')
            
            with open(F"{BASE_DIR}/userdata/backupcode/{username}.txt", "w") as f:
                for code in code_lists:
                    f.writelines(F"{code.text}\n")

