# import undetected_chromedriver as uc
from selenium import webdriver
from . import settings
import os


class Bot(webdriver.Chrome):

    def __init__(self, teardown: bool=False):
        self.teardown = teardown
        os.environ["PATH"] += settings.DRIVER_PATH
        super(Bot, self).__init__(options=settings.CHROME_OPTIONS)

    
    def __exit__(self, *args) -> None:
        if self.teardown:
            print("Exited gracefully")
            self.quit()


    def open_url(self) -> None:
        self.get(settings.BASE_URL)
