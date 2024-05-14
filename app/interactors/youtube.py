from playwright.async_api import async_playwright, expect, BrowserContext


class VideoNotFound(Exception):
    pass


async def youtube__get__page_content(*, url: str, context: BrowserContext):
    page = await context.new_page()
    await page.goto(url)
    await page.wait_for_load_state()

    try:
        await expect(page.get_by_text('Before you continue')).to_have_count(1)
        await page.locator('button[aria-label="Accept all"]').first.click()
        await page.wait_for_load_state()
    except AssertionError:
        pass

    url = await youtube__get__first_video(page=page)
    return url


async def youtube__get__channel_content(*, channel_name: str, context: BrowserContext):
    return await youtube__get__page_content(url=f"https://www.youtube.com/@{channel_name}/videos", context=context)


async def youtube__get__first_video(*, page):
    selector = f"a#video-title-link"
    locator = page.locator(selector)
    if await locator.count() == 0:
        raise VideoNotFound
    href = await locator.first.get_attribute("href")
    return f"https://www.youtube.com{href}"
