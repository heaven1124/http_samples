import requests
from lxml import etree


start_url = 'http://www.qianmu.org/ranking/905.htm'


# 请求下载网页
def fetch(url):
    re = requests.get(url)
    if re.status_code != 200:
        re.raise_for_status()
    return re.text.replace('\t', '')


# 处理大学详情页面
def parse_university(url):
    selector1 = etree.HTML(fetch(url))
    data = {}
    data['name'] = selector1.xpath('//div[@id="wikiContent"]/h1/text()')[0]
    table = selector1.xpath('//div[@id="wikiContent"]/div[@class="infobox"]/table')
    if table:
        table = table[0]
        keys = table.xpath('.//td[1]/p/text()')
        cols = table.xpath('.//td[2]')
        values = [' '.join(col.xpath('.//text()')) for col in cols]
        if len(keys) != len(values):
            return None
        data.update(zip(keys, values))
        return data

# 处理数据（存储到硬盘）
def process_data(data):
    if data:
        print(data)


if __name__ == '__main__':
    # 1.请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 2.提取列表页面的链接
    links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')

    for link in links:
        if not link.startswith('http://www.qianmu.org'):
            link = 'http://www.qianmu.org%s' % link
        # 3.提取详情页的信息
        data = parse_university(link)
        # 4.处理数据
        process_data(data)




