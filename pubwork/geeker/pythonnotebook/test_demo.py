import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup


async def get_web(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def post_web(session, url):
    with async_timeout.timeout(10):
        pdata = {'page.pageNo': 2, 'xmlname': '1462259560614', 'V_DATE': '2014-01-01', 'E_DATE': '2017-08-22'}
        async with session.post(url, data=pdata) as response:
            payload = {'key1': 'value1', 'key2': 'value2'}
            result = await response.text()
            html_obj = BeautifulSoup(result, 'lxml')
            mvalue = html_obj.select('#gisDataJson')
            print(type(mvalue[0]),mvalue[0]['value'])
            return mvalue


async def main():
    async with aiohttp.ClientSession() as session:
        html = await post_web(session, 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action')
        print(html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())