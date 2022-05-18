# Instagram Bot

Bot used to automate certain instagram (_web_) functions using [python](https://www.python.org/) and [selenium](https://www.selenium.dev/).

## Features
1.  #### Authentication
    - Login via username/password.
    - Continuously prompts for OTP in terminal if 2FA is enabled (SMS/APP) until passed.
    - Can save cookies of authenticated accounts and use them later to authenticate. *Can be changed.*
    - Turns off notification by default. *Can be changed.*

2.  #### Account Activity
    - Set/update account `name`, `username`, `bio`, `website`, `email`, `phone`
        >NOTE: When you change email address, you'll need to verify the new email with the link sent to you. Phone number cannot be changed when SMS-2FA is enabled. You either disable SMS-2FA using `disable_twofa()` method then update it or you update it using the `enable_sms_twofa()` method directly.

    - Change password. You need the old password along side.
    - Enable SMS-2FA. Only SMS-2FA can be enabled from instagram web.
    - Disable all 2FA. Both SMS and APP 2FA can be disabled from instagram web.
    - Retrieve and store backup codes for account with 2FA enabled.

3.  #### Basic OSINT
    - Get a targets `name`, `username`, `category`, `website` account `photo` url, number of `posts`, `followers`, `following` and `private` & `verified` state.


## Installation
Just simply clone this repository.

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
from instagramBot import config


with Bot(teardown=True) as bot:
    bot.open_url()
    via_cookies = InstagramLogin(driver=bot).login_via_cookies()
    
    if not via_cookies:
        InstagramLogin(driver=bot).login_via_login(username=config.SECURE["username"], password=config.SECURE["password"])

    
    InstagramProfile(driver=bot).disable_twofa()
```

...you will notice that

- The first 4 lines imports what we need from within instagramBot. 
- `with Bot(teardown=True) as bot:` we are running an instance of the `Bot()` class from the `instagramBot.bot` module, this is required because the `Bot()` class is our web driver instance and contains method to navigate to instagram website, We've alse passed `teardown=True` to gracefully terminate the bot after execution, **default is False**.
- `bot.open_url()` opens the webdriver and navigates to instagram website, this is where the login page is rendered.
- `via_cookies = InstagramLogin(driver=bot).login_via_cookies()` Loads cookies if available into the current webdriver session for the username supplied in your `config.LOGIN` found in `settings.py`. If the cookies are valid then user is authenticated. This method return a boolean value.
- `if not via_cookies:` if the user has no cookies or cookies could not authenticate the user.**expired cookies**
- `InstagramLogin(driver=bot).login_via_login(username=config.SECURE["username"], password=config.SECURE["password"])` then try to login with the username/password found in `config.LOGIN` provided in `settings.py` file. More on [settings.py](#settingspy-File) later.
- `InstagramProfile(driver=bot).disable_twofa()` take one arguement `driver=bot` which is the webdriver instance to operate on and calls the `disable_twofa()` method.

>NOTE: `InstagramLogin`, `InstagramProfile`, and `InstagramOSINT` takes one argument `driver`, which is the webdriver instance to operate on,
this should be the same instance that opens your web browser.


## Classes and methods

- `Bot()`
  - `open_url()`. Loads instagram url from gotten from `settings.py` file.

- `InstagramLogin()`. Takes the bot instance as argument.
  - `login_via_cookies()`. Takes no argument.
  - `login_via_login()`. Takes 3 arguments, `username`, `password` and `save_login`.

- `InstagramProfile()`. Takes the bot instance as argument.
  - `update_profile_email()`. Takes 1 argument `email`.
  - `update_profile_phone()`. Takes 1 argument `phone`.
  - `update_profile_username()`. Takes 1 argument `username`.
  - `update_profile_name()`. Takes 1 argument `name`.
  - `update_profile_website()`. Takes 1 argument `website`.
  - `update_profile_bio()`. Takes 1 argument `bio`.
  - `change_password()`. Takes 3 arguments `old_password`, `new_password`, `confirm_password`.
  - `disable_twofa()`. Take no argument.
  - `enable_sms_twofa()`. Takes 1 argument `phone`.
  - `get_backup_code()`. Take no argument.

- `InstagramOSINT()`. Takes the bot instance as argument.
  - `get_target_info()`. Takes 1 argument `save`.


## Settings.py File
This file can be eited but with *caution*. Look at [settings.py](./instagramBot/settings.py)
