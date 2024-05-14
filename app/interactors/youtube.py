from playwright.sync_api import sync_playwright, expect


class VideoNotFound(Exception):
    pass


def youtube__get__page_content(*, url):
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

    url = youtube__get__first_video(page=page)
    browser.close()
    return url


def youtube__get__channel_content(*, channel_name):
    return youtube__get__page_content(url=f"https://www.youtube.com/@{channel_name}/videos")


def youtube__get__first_video(*, page):
    selector = f"a#video-title-link"
    locator = page.locator(selector)
    if locator.count() == 0:
        raise VideoNotFound
    href = locator.first.get_attribute("href")
    return f"https://www.youtube.com{href}"
