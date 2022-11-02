import io

import urllib3.util
import uvicorn
from fastapi import FastAPI
from playwright.async_api import async_playwright
from starlette.responses import StreamingResponse, PlainTextResponse, Response

app = FastAPI()


@app.get("/playwright")
async def playwright_screenshot(url: str, width: int = 390, height: int = 844):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(ignore_https_errors=True, viewport={'width': width, 'height': height})
        page = await ctx.new_page()
        res: Response
        try:
            page.set_default_timeout(10000)
            await page.goto(str(urllib3.util.parse_url(url)))
            screenshot_bytes = await page.screenshot()
            res = StreamingResponse(content=io.BytesIO(screenshot_bytes), media_type="image/png")
        except TimeoutError:
            res = PlainTextResponse("请求超时", status_code=400)
        except NameError:
            res = PlainTextResponse("域名错误", status_code=400)
        finally:
            await page.close()
            await browser.close()
        return res


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        debug=True,
        log_level="info",
    )
