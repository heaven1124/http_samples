import os
from pprint import pprint
from urllib.request import urlretrieve

import requests
import re
from lxml import etree
import lxml.html
import tinycss
from tinycss.token_data import ContainerToken

url = 'http://www.dianping.com/shop/113942879'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
r = requests.get(url, headers=headers)

selector = etree.HTML(r.text)
plist = selector.xpath('//ul[@id="reviewlist-wrapper"]/li//p[@class="desc"]')
for p in plist:
    # 把节点对象转换成HTML源码
    source = lxml.html.tostring(p, encoding='unicode')
    # 去掉源码最外面的p标签
    source = source[16:-5]
    # 替换掉内部的span标签
    text = re.sub(r'<span class\"([a-zA-Z0-9\-]+)\"></span>', r'{{\1}}', source)
# 请求css文件
css_url = selector.xpath('//link[contains(@href, "svgtextcss")]/@href')[0]
css_resp = requests.get('http:' + css_url)
# 解析css文件
parser = tinycss.make_parser('page3')
ss = parser.parse_stylesheet(css_resp.text)
css_dict = {}
for rule in ss.rules:
    print(rule.selector[1].value, end=": ")
    # for selector in rule.selector:
    #     if isinstance(selector, ContainerToken):
    #         print(selector)
    #         continue
    selector = rule.selector[-1]
    if isinstance(selector, ContainerToken):
        css_class = selector.content[-1].value
    else:
        css_class = selector.value
    css_dict[css_class] = {}
    for d in rule.declarations:
        lst = []
        for v in d.value:
            if v.value == ' ':
                continue
            lst.append(v.value)
        css_dict[css_class][d.name] = lst
pprint(css_dict)


def down_svg(svg_url):
    svg_filename = os.path.basename(svg_url)
    svg_path = os.path.join('./svg/', svg_filename)
    urlretrieve('http:' + svg_url, svg_path)


for k, data in css_dict.items():
    if 'background-image' in data:
        down_svg(data['background-image'][0])