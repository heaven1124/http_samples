import requests
from lxml import etree
from urllib.parse import quote

keyword = 'iphone'
params = dict(
    keyword=keyword,
    enc='utf-8',
    wq=keyword,
    pvid='4e1832d54e9248bc9267caf8a10ff46a'
)
query_string = '&'.join('%s=%s' % (k, v) for k, v in params.items())
jd_url = 'https://search.jd.com/Search?' + query_string
url = 'http://10.0.0.48:8050/render.html?url=' + quote(jd_url)

r = requests.get(url)
r.encoding = 'utf-8'
selector = etree.HTML(r.text)

name_list = selector.xpath('//div[contains(@class, "p-name")]/a/em/text()')
prices = selector.xpath('//div[@class="p-price"]/strong/i/text()')

for name, price in zip(name_list, prices):
    print(name, price)
