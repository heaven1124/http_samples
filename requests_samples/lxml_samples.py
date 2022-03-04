from lxml import etree
import requests


html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1" cate="web">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2" cate="web">Lacie</a> and
<a href="http://example.com/tillie" class="father" id="link3"><price>Tillie</price></a>;
<a href="http://example.com/alan" class="brother" id="link4"><price>25</price></a>;
<a href="http://example.com/eric" class="mother" id="link5"><price>35</price></a>;
and they lived at the bottom of a well.</p>

<p class="book video sound">...</p>
<p class="book paper">more</p>
"""

selector = etree.HTML(html_doc)
# 取出class为story的节点下面所有的a标签的href属性值，
# "@"表示选取属性值
links = selector.xpath('//p[@class="story"]/a/@href')
for link in links:
    print(link)

se = etree.HTML(html_doc)
# //表示从任意子节点中选取，/表示从根节点选取，
# "./"表示从当前节点选取，"../"表示从父节点选取
print(se.xpath('//a/text()'))
print(se.xpath('//a[1]/@id'))
print(se.xpath('//a[last()]/@id'))
# 选取倒数第二个
print(se.xpath('//a[last()-1]/@id'))
# 选取前二个
print(se.xpath('//a[position()<3]/@id'))
# 选取cate属性等于web的
print(se.xpath('//a[@cate="web"]/text()'))
print(se.xpath('//a[price>30]/price/text()'))
# 选取所有class属性中包含book的p标签的class属性
print(se.xpath('//p[contains(@class, "book")]/@class'))









