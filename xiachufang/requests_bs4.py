import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests


r = requests.get('http://www.xiachufang.com/')
soup = BeautifulSoup(r.text, features="lxml")

img_list = []
for img in soup.select('img'):
    if img.has_attr('data-src'):
        img_list.append(img.attrs['data-src'])
    else:
        img_list.append(img.attrs['src'])
print(img_list)
# 初始化下载文件目录
imge_dir = os.path.join(os.curdir, 'images')
# if not os.path.isdir(imge_dir):
#     os.mkdir(imge_dir)
# 倒序遍历
for img in img_list[::-1]:
    o = urlparse(img)
    # 在图片链接中截取图片文件名
    # str.split('?')[0].split('/')[-1]
    filename = o.path[1:].split('@')[0]
    filepath = os.path.join(imge_dir, filename)
    # 如果有必要的话，循环创建目录
    # os.path.dirname()函数功能：去掉文件名，返回目录
    if not os.path.isdir(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))
    url = '%s://%s/%s' % (o.scheme, o.netloc, filename)

    resp = requests.get(url)
    with open(filepath, 'wb') as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)

