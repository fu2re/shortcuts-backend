import sys
import re
import requests
import logging
from typing import Union
from fastapi import FastAPI, Depends


app = FastAPI()


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class Cookies:
    instance = {}

    def __new__(cls):
        if not cls._instance:
            cls.instance = super().__new__(cls)
        return cls.instance


def get_cookies():
    return Cookies()


def renew_cookies(cookies, url):
   logger.info('Get new cookies: %s', x)

   browser = webkit.launch()
   context = browser.new_context()
   page = context.new_page()
   page.goto(url)
   
   cookies = context.cookies()


   cookies.instance = {}


@app.get("/waze-gm/ping")
def read_root():
    return "PONG"


@app.get("/waze-gm/{app}")
def read_item(app, url: str = None, cookies=Depends(get_cookies)):
    x = requests.get(url, allow_redirects=True, cookies=cookies).url
    logger.info('Full url: %s', x)
    if 'consent.google.com' in x:
      renew_cookies()
      x = requests.get(url, allow_redirects=True, cookies=cookies).url
      logger.info('Full url after second-attempt is: %s', x)
    try:
      lat = re.search("!3d(\-{0,1})(\d+\.\d+)", x).groups()[1]
      logger.info('Lat: %s', lat)
      lon = re.search("!4d(\-{0,1})(\d+\.\d+)", x).groups()[1]
      logger.info('Lon: %s', lon)
    except:
      return ""
    if app == "app":
       return f"waze://?ll={lat}%2C{lon}&navigate=yes"
    return f"https://www.waze.com/ul?ll={lat}%2C{lon}&navigate=yes" 
