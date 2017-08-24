# coding=UTF-8

from selenium import webdriver
from libs.webscraper.class_proxiesmanager import ProxyManager

pmanager = ProxyManager()
proxy = pmanager.random_http_proxy
print(''.join(['--proxy=',proxy]))

service_args = [''.join(['--proxy=',proxy]),'--proxy-type=http']
driver = webdriver.PhantomJS(executable_path="D:\\tools\\phantomjs\\bin\\phantomjs.exe",
                             service_args=service_args)

driver.get('http://impactfactor.cn/')
print(driver.title)