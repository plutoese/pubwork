# coding = UTF-8

import pandas as pd
from libs.webscraper.class_staticwebscraper import StaticSingleWebScraper

total_page_number = 5
search_web_template = 'http://www.dianping.com/search/category/1/10/g101r873p{}'

list_dataset = []
for i in range(1,total_page_number+1):

    web_scraper = StaticSingleWebScraper(web_site=search_web_template.format(i))
    web_scraper.scrape()

    bsobj = web_scraper.html_parser.bsobj
    all_shop = bsobj.select('#shop-all-list li')
    for shop in all_shop:
        shop_name = shop.select('.tit h4')[0].text
        if len(shop.select('.review-num b')) > 0:
            review_num = shop.select('.review-num b')[0].text
        else:
            review_num = None
        if len(shop.select('.mean-price b')) > 0:
            mean_price = shop.select('.mean-price b')[0].text
        else:
            mean_price = None
        if len(shop.select('.addr')) > 0:
            address = shop.select('.addr')[0].text
        else:
            address = None
        if len(shop.select('.comment-list b')) > 0:
            taste, enviroment, service = [item.text for item in shop.select('.comment-list b')]
        else:
            taste, enviroment, service = (None,None,None)
        print(shop_name,review_num,mean_price,address,taste,enviroment,service)
        list_dataset.append((shop_name,review_num,mean_price,address,taste,enviroment,service))
        print('***************')

dataset = pd.DataFrame(list_dataset,columns=['饭店名称','点评','人均价格','饭店地址','口味','环境','服务'])
print(dataset)
dataset.to_excel('d:/output.xlsx')

'''
for shop in all_shop.select('.tit'):
    print(shop)
    print('**********************************************')
    print(shop.select('h4'))'''
