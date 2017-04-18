# coding=UTF-8

"""
=========================================
电子邮件类
=========================================

:Author: glen
:Date: 2017.2.21
:Tags: mail
:abstract: 抓取12306火车票实时数据

**类**
==================
Mail
    收发邮件


**简介**
==================
收发邮件


**使用方法**
==================

"""

from envelopes import Envelope, GMailSMTP

class Mail:
    def __init__(self, from_addr=(u'cfzhang@163.com','glen')):
        self._from_addr = from_addr

    def send(self, to_addr=None, subject='', body='', attachment=None):
        envelope = Envelope(to_addr=to_addr, from_addr=self._from_addr, subject=subject, text_body=body)
        if attachment is not None:
            envelope.add_attachment(attachment)
        envelope.send('smtp.163.com',login='cfzhang@163.com',password='z1Yh29476801',tls=True)


if __name__ == '__main__':
    mail = Mail()
    mail.send(to_addr=[u'glen.zhang7@gmail.com'], subject='From Pluto', body=u'这是为你写的歌！')
