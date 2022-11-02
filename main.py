import io

import urllib3.util
import uvicorn
from fastapi import FastAPI
from playwright.async_api import async_playwright
from starlette.responses import StreamingResponse, PlainTextResponse

app = FastAPI()


@app.get("/playwright")
async def playwright_screenshot(url: str, width: int = 390, height: int = 844):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': width, 'height': height})
        try:
            page.set_default_timeout(5000)
            await page.goto(str(urllib3.util.parse_url(url)))
            screenshot_bytes = await page.screenshot()
        except TimeoutError:
            return PlainTextResponse("请求超时", status_code=400)
        await page.close()
        await browser.close()
        return StreamingResponse(content=io.BytesIO(screenshot_bytes), media_type="image/png")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        debug=True,
        log_level="info",
    )
