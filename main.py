from instagramBot.instagram_profile import InstagramProfile
from instagramBot.instagram_login import InstagramLogin
from instagramBot.instagram_osint import InstagramOSINT
from instagramBot.bot import Bot


with Bot() as bot:
    bot.open_url()
    via_cookies = InstagramLogin(driver=bot).login_via_cookies(username="everythinlethal")

    if not via_cookies:
        InstagramLogin(driver=bot).login_via_login(username="everythinlethal", password="EvtlEvtl@6060f914")

    InstagramProfile(driver=bot).get_backup_code(username="everythinlethal")