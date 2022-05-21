# This file should be edited as per your needs.
# Chrome is the default webdriver used for this program, please refer to
# https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# to install drivers for any specific browser supported by selenium.

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pathlib import Path

# Base dir refers to the current directory the instagramBot module is located.
# To refer to other directories within this module use "BASE_DIR / your/file/path" 
BASE_DIR = Path(__file__).parent


# Webdriver path is a flexible option to change location of drivers without having
# to update your code, and will work on multiple machines without requiring that
# each machine put the drivers in the same place. This used the "PATH" directory.
# you can add your specific web driver version in the driver folder.
DRIVER_PATH = F":{BASE_DIR}/drivers/" # Linux


# Instagram Urls
BASE_URL = "https://www.instagram.com"
CHANGE_PASSWORD_URL = F"{BASE_URL}/accounts/password/change/"
ACCOUNT_EDIT_URL = F"{BASE_URL}/accounts/edit/"
PRIVACY_SECURITY_URL = F"{BASE_URL}/accounts/privacy_and_security/"
TWOFA_URL = F"{BASE_URL}/accounts/two_factor_authentication/"


# User-Agents, add/edit as required.
UA_ANDROID = "Mozilla/5.0 (Linux; Android 9; A5_Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36"
UA_IPHONE_XS = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"

# This settings is used to emulate a mobile device
MOBILE_EMULATION = {
    "deviceMetrics": { "width": 414, "height": 896, "pixelRatio": 3.0 },
    "userAgent": UA_ANDROID
}


# Chrome driver options.
# visit: https://chromedriver.chromium.org/ for better understanding
CHROME_OPTIONS = ChromeOptions()
# CHROME_OPTIONS.add_argument("--headless")
# CHROME_OPTIONS.add_argument("--window-size=1600,900")

# Firefox driver options
FIREFOX_OPTIONS = FirefoxOptions()
FIREFOX_OPTIONS.add_argument("--headless")