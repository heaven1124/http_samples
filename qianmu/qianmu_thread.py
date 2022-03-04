import time
import sys
import requests
import threading
import signal
from queue import Queue
from lxml import etree
import redis


start_url = 'http://www.qianmu.org/2022USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
# link_queue = Queue()
threads = []
THREADS_NUM = 10
download_pages = 0
r = redis.Redis(host='10.0.0.48',
                password='123')
thread_on = True


# 请求下载网页
def fetch(url):
    try:
        re = requests.get(url, timeout=10)
        if re.status_code != 200:
            re.raise_for_status()
        global download_pages
        download_pages += 1
        return re.text.replace('\t', '')
    except Exception:
        print('error raised when fetch %s' % url)


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


def download(i):
    while thread_on:
        # 阻塞，直到从队列里获取一条消息
        # link = link_queue.get()
        link = r.lpop('qianmu.queue')
        if link:
            data = parse_university(link)
            process_data(data)
            print('remaining queue: %s' % r.llen('qianmu.queue'))
        time.sleep(0.2)
    print('Thread-%s exit now' % i)


def sigint_handler(signum, frame):
    print('received Ctrl+C, wait for exit gracefully')
    global thread_on
    thread_on = False


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     start_url = sys.argv[1]
    # 1.请求入口页面
    selector = etree.HTML(fetch(start_url))
    # 2.提取列表页面的链接
    links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')

    for link in links:
        if not link.startswith('http://www.qianmu.org'):
            link = 'http://www.qianmu.org%s' % link
        # link_queue.put(link)
        if r.sadd('qianmu.seen', link):
            r.rpush('qianmu.queue', link)
    # else:
    # 启动线程，并将线程对象放入一个列表保存
    for i in range(THREADS_NUM):
        t = threading.Thread(target=download, args=(i+1,))
        t.start()
        threads.append(t)

    # 捕捉终端CTRL+c产生的SIGINT信号
    signal.signal(signal.SIGINT, sigint_handler)
    # 阻塞队列，直到队列被清空
    # link_queue.join()

    # 向队列发送n个None，以通知线程退出
    # for i in range(THREADS_NUM):
    #     link_queue.put(None)

    # 退出线程
    for t in threads:
        t.join()



