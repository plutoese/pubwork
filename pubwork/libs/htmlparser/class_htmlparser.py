# coding=UTF-8

# --------------------------------------------------------------
# class_htmlparser文件
# @class: HtmlParser类
# @introduction: HtmlParser类用来解析html对象
# @dependency: bs4及re包
# @author: plutoese
# @date: 2016.06.24
# --------------------------------------------------------------

from bs4 import BeautifulSoup
import re


class HtmlParser:
    """HtmlParser类用来解析html对象

    :param str htmlcontent: html的字符串
    :return: 无返回值
    """
    def __init__(self,html_content=None):
        if isinstance(html_content,BeautifulSoup):
            self._bs_obj = html_content
        else:
            self._html_content = html_content
            self._bs_obj = BeautifulSoup(self._html_content, "lxml")

    def table(self,css=None):
        """ 返回表格的数据

        :param css: table的css选择器
        :return: 表格的列表
        """
        table = []
        tds = None
        if css is not None:
            tds = self._bs_obj.select(''.join([css,' > tr']))

        for item in tds:
            table.append([re.sub('\s+','',unit.text) for unit in item.select('td')])

        return table

    @property
    def html(self):
        return self._html_content

    @property
    def bsobj(self):
        return self._bs_obj

    @property
    def title(self):
        return self._bs_obj.title.string


if __name__ == '__main__':
    pass

