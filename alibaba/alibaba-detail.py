#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################
#    专业术语    #
##################
# 求购   buy     #
# 商品   product #
# 交易   deal    #
# 支付   pay     #
# 收货   receipt #
# 采购商 buyer   #
# 供应商 supplier#
# 询价   inquiry #
# 报价   quote   #
# 发票   invoice #
# 截止   expire  #
# 日期   date    #
# 数量   count   #
# 地址   address #
##################

from lxml import html
from urllib2 import urlopen
from pprint import pprint

def parse(txt):

    dom = html.fromstring(txt)

    buy_title = dom.xpath('//div[@class="mod-title"]/h1/text()')
    buy_type = dom.xpath(u'//ul[@class="goods-list"]/li[contains(.,"采购类型：")]/div/span/text()')
    inquiry_date = dom.xpath(u'//ul[@class="goods-list"]/li[contains(.,"询价日期：")]/div/span/text()')
    receipt_date = dom.xpath(u'//div[@class="receive-date"]/span[starts-with(.,"期望收货：")]/text()')
    expire_date = dom.xpath('//span[@class="countdown-date"]/em/text()')
    quote_count = dom.xpath(u'//div[contains(@class,"extrainfo")]//li[contains(.,"收到报价")]/span/text()')

    buy_list = []
    for tr in dom.xpath('//div[@class="inquiry-list"]/table//tr[td]'):
        name, quantity, memo, img = tr.xpath('td')
        buy_list.append({
            'name':name,
            'quantity':quantity,
            'memo':memo,
            'img': img
        })

    deal_method = dom.xpath(u'//div[@class="title" and .="交易方式："]/following-sibling::div[1]')
    invoice_needed = dom.xpath(u'//div[@class="title" and .="发票要求："]/following-sibling::div[1]')
    receipt_address = dom.xpath(u'//div[@class="title" and .="收货地："]/following-sibling::div[1]')
    extra_info = dom.xpath(u'//div[@class="title" and .="补充说明："]/following-sibling::div[1]')

    quote_list = []
    for tr in dom.xpath('//table[@class="quotation"]//tr[td]'):
        quote_date, supplier, area, quote_article = tr.xpath('td')
        quote_list.append({
            'quote_date': quote_date,
            'supplier': supplier,
            'area': area,
            'quote_article': quote_article
        })

    return {
            'buy_title': buy_title,
            'buy_list': buy_list,
            'quote_list': quote_list,
            '...': '...'
    }

if __name__=='__main__':

    url = 'http://go.1688.com/buyoffer/33027238.htm'
    txt = urlopen(url).read().decode('gbk')
    item = parse(txt)
    pprint(item)

