import asyncio
import aiohttp
from sheldon.webscraper.class_proxymanager import ProxyManager


async def example():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            get('http://www.sina.com.cn/', session),
            get('http://datacenter.mep.gov.cn/index', session),
            get('http://www.dgtle.com/portal.php', session)
        )
        print(results)


async def get(url, session):
    try:
        async with session.get(url, proxy=ProxyManager().random_proxy) as resp:
            return await resp.text()
    except:
        return await get(url,session)


loop = asyncio.get_event_loop()
loop.run_until_complete(example())