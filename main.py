from instagramBot.instagram_profile import InstagramProfile
from instagramBot.instagram_login import InstagramLogin
from instagramBot.instagram_osint import InstagramOSINT
from instagramBot.bot import Bot
from instagramBot import settings


with Bot() as bot:
    bot.open_url()
    via_cookies = InstagramLogin(driver=bot).login_via_cookies()
    
    if not via_cookies:
        InstagramLogin(driver=bot).login_via_login(username=settings.SECURE["username"], password=settings.SECURE["password"])

    
    InstagramProfile(driver=bot).disable_twofa()