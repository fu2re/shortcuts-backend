import playwright
from playwright.sync_api import sync_playwright

from app.logger import logger


class Cookies:
    instance = None
    storage = {}

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def update(self, cookies):
        self.storage[app] = cookies

    def get_cookies(self, app):
        return self.storage.get(app, {})


def get_cookie_storage():
    return Cookies()


def get_new_cookies(*, cookie_storage: Cookies, url: str):
    logger.info('Get new cookies: %s', url)

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)

    selector = f"span:has-text('Accept All')"
    # page.wait_for_selector(selector)
    page.click(selector)
    page.wait_for_load_state()

    page.url()

    browser.close()

    cookies = context.cookies()
    print(cookies)
    logger.info(cookies)
    # url
    cookie_storage.update(cookies=cookies)
