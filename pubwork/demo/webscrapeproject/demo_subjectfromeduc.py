# coding = UTF-8

import re
from libs.webscraper.class_staticwebscraper import StaticSingleWebScraper

web_site = 'http://www.cdgdc.edu.cn/xwyyjsjyxx/xwsytjxx/xk/xkzyml/276559.shtml'

scraper = StaticSingleWebScraper(web_site=web_site,encoding='GBK')
scraper.scrape(verify=False)
print(scraper.html_parser.title)

bs_obj = scraper.html_parser.bsobj
print(scraper.html_parser.bsobj.select('.show > table'))

mytds = scraper.html_parser.bsobj.select('.show > table')

table = []
for tds in mytds:
    for item in tds:
        table.append([re.sub('\s+', '', unit.text) for unit in item.select('td')])

num1 = set()
num2 = set()
num3 = set()

for tab in table:
    for item in tab:
        if re.match('^\d{2}$',re.sub('\s+','',item)):
            num1.add(re.sub('\s+','',item))
        if re.match('^\d{4}$',re.sub('\s+','',item)):
            num2.add(re.sub('\s+','',item))

print('total number one: ',len(num1))
print('total number two: ',len(num2))

website2 = 'http://www.cdgdc.edu.cn/xwyyjsjyxx/xwsytjxx/xk/xkzyml/282917.shtml'

scraper = StaticSingleWebScraper(web_site=website2,encoding='GBK')
scraper.scrape(verify=False)
print(scraper.html_parser.title)
print(scraper.html_parser.bsobj.select('.show > table'))
mytds = scraper.html_parser.bsobj.select('.show > table')

table = []
for tds in mytds:
    for item in tds:
        table.append([re.sub('\s+', '', unit.text) for unit in item.select('td')])
print(table[1])

nu1 = set()
nu2 = set()

for item in table[1]:
    if re.match('^\d{2}$',re.sub('\s+','',item)):
        nu1.add(re.sub('\s+','',item))
    if re.match('^\d{4}$',re.sub('\s+','',item)):
        nu2.add(re.sub('\s+','',item))

print('total number one: ',len(nu1))
print('total number two: ',len(nu2))