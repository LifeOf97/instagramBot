# Instagram Bot

Bot used to automate certain instagram (_web_) functions using [python](https://www.python.org/) and [selenium](https://www.selenium.dev/).

## Features
1.  #### Authentication
    - Login via username/password or saved cookies.
    - Continuously prompts for OTP in terminal if 2FA is enabled (SMS/APP) until passed.
    - Can save cookies of authenticated accounts and use them later to authenticate. *Can be changed.*
    - Turns off notification by default. *Can be changed.*

2.  #### Account Activity
    - Set/update account `name`, `username`, `bio`, `website`, `email`, `phone`
        >NOTE: When you change email address, you'll need to verify the new email with the link sent to you by instagram. Phone number cannot be changed when SMS-2FA is enabled. You either disable SMS-2FA using `disable_twofa()` method then update it or you update it using the `enable_sms_twofa()` method directly.

    - Change password. You need the old password along side.
    - Enable SMS-2FA. Only SMS-2FA can be enabled from instagram web.
    - Disable all 2FA. Both SMS and APP 2FA can be disabled from instagram web.
    - Retrieve and store backup codes for account with 2FA enabled.

3.  #### Basic OSINT
    - Get a targets `name`, `username`, `category`, `website` account `photo` url, number of `posts`, `followers`, `following` and `private` & `verified` state.


## Installation
Just clone this repository.

```bash

# clone repo
git clone https://github.com/realestKMA/instagramBot.git

# move into newly cloned repo
cd instagramBot/

# i recommend you run this bot in a python virtual environment and install all dependencies.
# in instagramBot directory run
python -m venv venv

# activate virtual environment
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

#### Requirements
- Python 3.7+


## Usage
>NOTE: The words webdriver and web browser are used interchangeably in this context, therefore means the same thing.

From the `main.py` example below...

```python

from instagramBot.instagram_profile import InstagramProfile
from instagramBot.instagram_login import InstagramLogin
from instagramBot.bot import Bot


with Bot(teardown=True) as bot:
    bot.open_url()
    via_cookies = InstagramLogin(driver=bot).login_via_cookies(username="your-username")
    
    if not via_cookies:
        InstagramLogin(driver=bot).login_via_login(username="your-username", password="your-password")

    
    InstagramProfile(driver=bot).disable_twofa()
```

...you will notice that

- The first 4 lines imports what we need from within instagramBot. 
- `with Bot(teardown=True) as bot:` we are running an instance of the `Bot()` class from the `instagramBot.bot` module, this is required because the `Bot()` class is our web driver instance and contains method to navigate to instagram website, We've alse passed `teardown=True` to gracefully terminate the bot after execution, **default is False**.
- `bot.open_url()` opens the webdriver and navigates to instagram website, this is where the login page is rendered.
- `via_cookies = InstagramLogin(driver=bot).login_via_cookies()` Loads cookies of the specified username if available into the current webdriver session. If the cookies are valid/not expired then user is authenticated. Returns `True` / `False`.
- `if not via_cookies:` if the user has no cookies or cookies could not authenticate the user.**expired cookies**
- `InstagramLogin(driver=bot).login_via_login(username="your-username", password="your-password"`. Try to login with the username/password provided if cookies failed or is not present. Returns `True` / `False`.
- `InstagramProfile(driver=bot).disable_twofa()`. InstagramBot() takes one arguement `driver=bot` which is the webdriver instance to operate on and calls the `disable_twofa()` method.

>NOTE: `InstagramLogin`, `InstagramProfile`, and `InstagramOSINT` takes one argument `driver`, which is the webdriver instance to operate on,
this should be the same instance that opens your web browser.


## Classes and methods

- `Bot()`
  - `open_url()`. Loads instagram url from gotten from `settings.py` file.

    > NOTE: `Bot()` class uses the firefox `geckodriver` and `FIREFOX_OPTIONS` by default. To change to your prefered driver, please follow the steps outlined below.
    - Download your prefered web browser driver from [selenium drivers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).
    - Extract the driver from the downloaded folder and move/copy it to the `drivers/` directory in InstagramBot.
    - Open the `bot.py` file and change the inherited webdriver `Bot(webdriver.YouBrowser_name)`.
    - Also change the `options` in `super().__init__()` to your web browsers options in `settings.py` file.


- `InstagramLogin()`. Takes the `bot` instance as argument.
  - `login_via_cookies()`. Takes 1 argument `username`.
  - `login_via_login()`. Takes 3 arguments, `username`, `password` and `save_login`.


- `InstagramProfile()`. Takes the bot instance as argument.
  - `update_profile_email()`. Takes 1 argument `email`.
  - `update_profile_phone()`. Takes 1 argument `phone`.
  - `update_profile_username()`. Takes 1 argument `username`.
  - `update_profile_name()`. Takes 1 argument `name`.
  - `update_profile_website()`. Takes 1 argument `website`.
  - `update_profile_bio()`. Takes 1 argument `bio`.
  - `change_password()`. Takes 3 arguments `old_password`, `new_password` and `confirm_password`.
  - `disable_twofa()`. Takes no argument.
  - `enable_sms_twofa()`. Takes 1 argument `phone`.
  - `get_backup_code()`. Takes 1 argument `username`.

- `InstagramOSINT()`. Takes the bot instance as argument.
  - `get_target_info()`. Takes 1 argument `save`.


## Settings.py File
This file can be eited but with *caution*. Look at [settings.py](./instagramBot/settings.py)
