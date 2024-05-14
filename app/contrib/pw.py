import playwright
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from app.logger import logger


class PW:
    instance = None
    pw = None
    browser = None
    context = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    async def start(self):
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=True)
        self.context = await self.browser.new_context(locale="en")


async def get_context():
    pw = PW()
    await pw.start()
    return pw.context

