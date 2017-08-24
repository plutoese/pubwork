# coding = UTF-8

import requests
import re

baidu_key = 'yourkey'
addresses = [('上海','复旦大学'),('北京','清华大学')]
web_fmt = 'http://api.map.baidu.com/geocoder/v2/?callback=renderOption&output=json&address={}&city={}&ak={}'

for addr in addresses:
    content = requests.get(web_fmt.format(addr[1],addr[0],baidu_key)).text
    split_str_by_lng = re.split('lng\":',content)[1]
    lng, *rest = re.split(',\"',split_str_by_lng)
    split_str_by_lat = re.split('\":',rest[0])
    lat, *rest = re.split('\}',split_str_by_lat[1])
    print(content)
    print(lng,lat)
