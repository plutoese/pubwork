# coding = UTF-8

from selenium import webdriver

driver = webdriver.Firefox(executable_path=r'D:\tools\firefox\firefox.exe')
driver.get("http://www.python.org")