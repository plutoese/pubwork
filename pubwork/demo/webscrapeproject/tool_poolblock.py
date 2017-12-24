# coding = UTF-8

import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()


def get_web(url):
    r = requests.get(url)
    print(r.text)

async def fetch_urls(urls):
    return asyncio.gather(*[loop.run_in_executor(executor, get_web, url) for url in urls])

loop.run_until_complete(fetch_urls(['http://www.sina.com.cn','http://www.jd.com','https://www.zhibo8.cc/']))