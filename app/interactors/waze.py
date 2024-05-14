import re
from enum import Enum

from playwright.sync_api import sync_playwright, expect

from app.logger import logger


class InvalidCoords(Exception):
    pass


class LinkType(Enum):
    web = "web"
    app = "app"


def google_maps_link__get__coordinates(*, url):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.wait_for_load_state()

    try:
        expect(page.get_by_text('Before you continue')).to_have_count(1)
        page.locator('button[aria-label="Accept all"]').first.click()
        page.wait_for_load_state()
    except AssertionError:
        pass

    coords = google_maps_link__parse__coordinates(full_url=page.url)

    browser.close()
    return coords


def google_maps_link__parse__coordinates(*, full_url):
    logger.info('Parse: %s', full_url)
    try:
        lat = re.search("!3d(\-{0,1})(\d+\.\d+)", full_url).groups()[1]
        logger.info('Lat: %s', lat)
        lon = re.search("!4d(\-{0,1})(\d+\.\d+)", full_url).groups()[1]
        logger.info('Lon: %s', lon)
    except KeyError:
        raise InvalidCoords
    return lat, lon


def google_maps_link__convert_to__waze_link(*, url: str, link_type: LinkType = LinkType.web):
    try:
        lat, lon = google_maps_link__get__coordinates(url=url)
    except InvalidCoords:
        logger.error("Unable to get coordinates")
        return ""

    if link_type == LinkType.app:
        return f"waze://?ll={lat}%2C{lon}&navigate=yes"

    return f"https://www.waze.com/ul?ll={lat}%2C{lon}&navigate=yes"
