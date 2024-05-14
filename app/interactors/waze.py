import re
from enum import Enum
from playwright.async_api import async_playwright, expect

from app.logger import logger


class InvalidCoords(Exception):
    pass


class LinkType(Enum):
    web = "web"
    app = "app"


async def google_maps_link__get__coordinates(*, url):
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(locale="en")
    page = await context.new_page()
    await page.goto(url)
    await page.wait_for_load_state()

    try:
        await expect(page.get_by_text('Before you continue')).to_have_count(1)
        await page.locator('button[aria-label="Accept all"]').first.click()
        await page.wait_for_load_state()
        await expect(page.get_by_text('Sign in')).to_have_count(1)
        logger.info("Terms accepted")
    except AssertionError:
        pass

    await page.wait_for_url(re.compile(r".+/@.+"))
    coords = google_maps_link__parse__coordinates(full_url=page.url)

    await browser.close()
    return coords


def google_maps_link__parse__coordinates(*, full_url):
    logger.info('Parse: %s', full_url)

    try:
        lat = re.search("!3d(\-{0,1}\d+\.\d+)", full_url).groups()[0]
        lon = re.search("!4d(\-{0,1}\d+\.\d+)", full_url).groups()[0]
    except (KeyError, AttributeError):
        if match := re.search("@(\-{0,1}\d+\.\d+),(\-{0,1}\d+\.\d+)", full_url):
            lat, lon = match.groups()
        else:
            raise InvalidCoords

    logger.info('Lat: %s', lat)
    logger.info('Lon: %s', lon)
    return lat, lon


async def google_maps_link__convert_to__waze_link(*, url: str, link_type: LinkType = LinkType.web):
    try:
        lat, lon = await google_maps_link__get__coordinates(url=url)
    except InvalidCoords:
        logger.error("Unable to get coordinates")
        return ""

    if link_type == LinkType.app:
        return f"waze://?ll={lat}%2C{lon}&navigate=yes"

    return f"https://www.waze.com/ul?ll={lat}%2C{lon}&navigate=yes"
