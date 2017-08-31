import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
import json
from sheldon.webscraper.class_proxymanager import ProxyManager
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

conn = MonCollection(mongodb='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/',
                     database='scraperdata', collection_name='airqualityfromMin').collection

async def get_web(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def post_web(session, url, pagenum):
    try:
        pdata = {'page.pageNo': pagenum, 'xmlname': '1462259560614', 'V_DATE': '2014-01-01', 'E_DATE': '2017-08-20'}
        proxy = ProxyManager().random_proxy
        print('Start Proxy... ',proxy)
        async with session.post(url, data=pdata, proxy=ProxyManager().random_proxy) as response:
            result = await response.text()
            html_obj = BeautifulSoup(result, 'lxml')
            mvalue = html_obj.select('#gisDataJson')
            page_data = json.loads(mvalue[0]['value'])
            for item in page_data:
                print(item)
                found = conn.find_one(item)
                if found is None:
                    conn.insert_one(item)
            return mvalue[0]['value']
    except:
        return await post_web(session, url, pagenum)


async def main(scope):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[post_web(session, 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action', i) for i in scope])

loop = asyncio.get_event_loop()

for i in range(2001,3000,10):
    print([num for num in range(i,i+10)])
    loop.run_until_complete(main(range(i,i+10)))