import bs4
from bs4 import BeautifulSoup


html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, features="html.parser")
# print(soup.prettify())
print(soup.title)
print(type(soup.title))
print(dir(soup.title))
print(soup.title.text)
print(soup.a.attrs['href'])
print(list(soup.p.children))
print(list(soup.p.children)[0].text)
print(soup.a.has_attr('href'))
print(soup.find_all('a'))
for a in soup.find_all('a'):
    print(a.attrs['href'])
print(soup.find(id='link1'))
print(soup.get_text())
# 支持css选择器，选择class为story的节点
print(soup.select('.story'))
# 选择class为story的节点下面的a标签
print(soup.select('.story a'))
print(soup.select('#link1'))
# 使用lxml作为bs4的解析器，运行速度快，因为lxml是用c语言开发的
soup_lxml = BeautifulSoup(html_doc, features="lxml")
print('########', soup_lxml.a)

