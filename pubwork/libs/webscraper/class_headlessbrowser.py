# coding=UTF-8

# --------------------------------------------------------------
# class_headlessbrowser文件
# @class: HeadlessBrowser类
# @introduction: HeadlessBrowser类用PhantomJS或firefox来执行网站动作和数据抓取
# @dependency: selenium包
# @author: plutoese
# @date: 2016.06.28
# --------------------------------------------------------------

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from libs.webscraper.class_proxiesmanager import ProxyManager
from selenium.common.exceptions import NoSuchElementException


class HeadlessBrowser:
    """ HeadlessBrowser类用PhantomJS或firefox来执行网站动作和数据抓取

    :param str proxy: proxy的地址，形式如'58.20.128.123:80'
    :return: 无返回值
    """
    def __init__(self,proxy=None,proxy_type='http',timeout=0,type=0):
        # 设置代理服务器
        if proxy is not None:
            print('proxy: ',proxy,', proxy type: ',proxy_type)
            # 如果type=0，则用PhantomJS，若type=1，则用firefox
            if type < 1:
                service_args = [''.join(['--proxy=',proxy]),''.join(['--proxy-type=',proxy_type])]
                self.browser = webdriver.PhantomJS(executable_path="D:\\tools\\phantomjs\\bin\\phantomjs.exe",service_args=service_args)
            else:
                self.__proxy = Proxy({'proxyType':ProxyType.MANUAL,
                                      'httpProxy':proxy,
                                      'httpsProxy':proxy,
                                      'ftpProxy':proxy,
                                      'sslProxy':proxy,
                                      'noProxy':''})
                self.browser = webdriver.Firefox(proxy=self.__proxy)
        else:
            if type < 1:
                self.browser = webdriver.PhantomJS(executable_path="D:\\tools\\phantomjs\\bin\\phantomjs.exe")
            elif type == 1:
                self.browser = webdriver.Firefox(executable_path="D:\\tools\\firefox\\firefox.exe")
            else:
                self.browser = webdriver.Ie()

        # 等待
        if timeout > 0:
            self.browser.implicitly_wait(timeout)
        # 设置get的timeout
        self.browser.set_page_load_timeout(30)
        # 最大化浏览器
        self.browser.maximize_window()
        self.pages = dict()
        self.current_window_handle = None
        self.window_handles = None

    def surf(self,website=None,ready_check=None):
        """ 浏览某网站

        :param str website: 网站地址
        :param int time_out: 超时设置
        :return: 无返回值
        """
        print('Starting load ',website)
        try:
            self.browser.get(website)
        except Exception:
            return False

        print('Loading......')
        if ready_check is not None:
            if self.is_ready(locator=ready_check):
                self.pages[self.browser.current_window_handle] = {'url':self.browser.current_url,
                                                                  'title':self.browser.title,
                                                                  'parent':None}
                self.current_window_handle = self.browser.current_window_handle
                self.window_handles = set(self.browser.window_handles)
                return True
            else:
                print('Not Ready')
                return False

    def is_ready(self,locator,timeout=20):
        """ 验证页面是否载入完成

        :param locator: 页面完成检验标志
        :param timeout: 超时设置
        :return: 是否载入完成
        :rtype: bool
        """
        try:
            print('Test Ready...')
            WebDriverWait(self.browser,timeout).until(expected_conditions.visibility_of_element_located(locator))
            print('Test Done...')
            return True
        except TimeoutException:
            print('TimeOut!')
            return False

    def locate(self,css_selector=None,id=None,xpath=None,link_text=None):
        """ 定位页面元素

        :param str css_selector: css选择器
        :param str id: id选择
        :param str xpath: xpath选择
        :param str link_text: 连接文本
        :return: 返回定位
        :rtype: selenium.webdriver.remote.webelement.WebElement
        """
        try:
            if css_selector is not None:
                return self.browser.find_element_by_css_selector(css_selector)
            if id is not None:
                return self.browser.find_element_by_id(id)
            if xpath is not None:
                return self.browser.find_element_by_xpath(xpath)
            if link_text is not None:
                return self.browser.find_element_by_link_text(link_text)
        except NoSuchElementException:
            return False

    def get_text(self,location,beautiful=False):
        """ 返回文本

        :param str,selenium.webdriver.remote.webelement.WebElement location: 网页定位
        :param bool beautiful: 是否返回beautiful soup对象
        :return: 返回页面元素
        :rtype: str, Beautiful soup
        """
        if isinstance(location,str):
            location = self.locate(css_selector=location)

        if beautiful:
            return BeautifulSoup(location.text,'lxml')
        else:
            return location.text

    def interact_one_time(self,location,send_text=None,click=False,select_text=None):
        """ 与页面交互

        :param str,selenium.webdriver.remote.webelement.WebElement location: 页面元素位置
        :param str send_text: 发送文本
        :param bool click: 是否点击
        :param str select_text: 选择文本
        :return: 无返回值
        """
        if isinstance(location,str):
            location = self.locate(css_selector=location)

        if click is True:
            location.click()
        if send_text is not None:
            location.clear()
            location.send_keys(send_text)
        if select_text is not None:
            Select(location).select_by_visible_text(select_text)

        tmp_handles = self.browser.window_handles
        handle = tmp_handles[len(tmp_handles) - 1]
        if handle not in self.window_handles:
            self.window_handles.add(handle)
            self.browser.switch_to.window(handle)
            self.pages[handle] = {'url':self.browser.current_url,
                                  'title':self.browser.title,
                                  'parent':self.current_window_handle}
            self.current_window_handle = handle

    def switch(self,iframe=None):
        """ 转换网页框架

        :param str iframe: 网页框架名称
        :return: 无返回值
        """
        if iframe is not None:
            self.browser.switch_to.frame(iframe)

    def switch_to_parent(self,close=True):
        """ 转换到父页面

        :param bool close: 是否关闭子页面
        :return: 无返回值
        """
        parent_handle = self.pages[self.current_window_handle]['parent']
        if close:
            self.window_handles.remove(self.current_window_handle)
            self.close()
        self.browser.switch_to.window(parent_handle)
        self.current_window_handle = parent_handle

    def close(self):
        """ 关闭当前浏览器

        :return: 无返回值
        """
        self.browser.close()

    def quit(self):
        """ 退出浏览器

        :return: 无返回值
        """
        self.browser.quit()

if __name__ == '__main__':
    pmanager = ProxyManager()
    proxy = pmanager.random_http_proxy
    browser = HeadlessBrowser(proxy=None, timeout=2, type=1)
    browser.surf('http://epub.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ',ready_check=(By.CSS_SELECTOR,'#bottom'))
    browser.interact_one_time(location=r'#\31 _4 > a:nth-child(1)',click=True)
    print(browser.get_text(location='.zySearch'))
    time.sleep(2)
    browser.close()

    '''
    browser.surf('https://www.hqms.org.cn/usp/roster/index.jsp',
                 ready_check=(By.CSS_SELECTOR,'.table_result'))
    print('I am starting Action!')
    browser.interact_one_time(location='.province_select',select_text='河北省')
    browser.interact_one_time(location='#btn_search',click=True)
    time.sleep(10)
    print('here')
    print(browser.get_text(location='.table_result'))
    browser.quit()
    #browser.surf('http://epub.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ')
    #browser.interact_one_time(location=browser.locate('.leftinside > ul:nth-child(1) > li:nth-child(1) > p:nth-child(2) > a:nth-child(3)'),click=True)
    #print(browser.get_text('.txt0'))
    #browser.interact_one_time(location=browser.locate('div.bg_white:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'),click=True)
    #print(browser.current_window_handle)
    '''
    '''
    university = '北京大学'
    print(''.join(['td > a[title="',university,'"]']))
    time.sleep(10)
    browser.surf('http://gkcx.eol.cn/soudaxue/queryProvinceScore.html',
                 ready_check=(By.CSS_SELECTOR,''.join(['td > a[title="',university,'"]'])))
    browser.quit()'''
