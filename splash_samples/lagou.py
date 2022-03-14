import requests
from lxml import etree
from urllib.parse import quote, urlencode

keyword = '爬虫'

lagou_url = 'https://www.lagou.com/wn/jobs?labelWords=&fromSearch=true&suginput=&kd=%s' % keyword
url = 'http://10.0.0.48:8050/render.html?url=' + quote(lagou_url)

r = requests.get(url)
r.encoding = 'utf-8'
selector = etree.HTML(r.text)

name_list = selector.xpath('//div[contains(@class, "p-name")]/a/em/text()')
prices = selector.xpath('//div[@class="p-price"]/strong/i/text()')

for name, price in zip(name_list, prices):
    print(name, price)
