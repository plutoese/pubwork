# -----------------------------------------------------------------------------------------
# 大众点评网饭店数据搜集程序
#
# 需填写的参数如下：
# 1. 变量search_web_template,填写搜索的网页地址，并在其后添加'{}'，
# 例如搜索网址为http://www.dianping.com/search/category/1/10/g101r865，
# 则search_web_template='http://www.dianping.com/search/category/1/10/g101r865{}'
# 2. 变量total_page_number，填写搜索结果共有几页，例如搜索结果共分5页，则total_page_number=5
# 3. 变量output_file,填写输出Excel文件名称，例如output='meilongrestaurant.xlsx'
#
# 最终生成的Excel文件在/output目录下
# ------------------------------------------------------------------------------------------

import pandas as pd
from libs.webscraper.class_staticwebscraper import StaticSingleWebScraper

# 参数，需用户自定义
search_web_template = 'http://www.dianping.com/search/category/1/10/g101r873p{}'
total_page_number = 5
output_file = 'meilongrestaurant.xlsx'

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
        list_dataset.append((shop_name,review_num,mean_price,address,taste,enviroment,service))

dataset = pd.DataFrame(list_dataset,columns=['饭店名称','点评','人均价格','饭店地址','口味','环境','服务'])

#dataset.to_excel(''.join(['./',output_file]))