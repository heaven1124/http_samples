import os
import re
from io import BytesIO
from urllib.parse import urlparse
from pycurl import Curl


buffer = BytesIO()
c = Curl()
c.setopt(c.URL, 'http://www.xiachufang.com/')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
text = body.decode('utf-8')

img_list = re.findall(r'src=\"(http://i2\.chumg\.com/\w+\.jpg)',
                      text)
# 初始化下载文件目录
imge_dir = os.path.join(os.curdir, 'images')
# if not os.path.isdir(imge_dir):
#     os.mkdir(imge_dir)
# 倒序遍历
for img in img_list[::-1]:
    o = urlparse(img)
    # 在图片链接中截取图片文件名
    # str.split('?')[0].split('/')[-1]
    filename = o.path[1:]
    filepath = os.path.join(imge_dir, filename)
    # 如果有必要的话，循环创建目录
    # os.path.dirname()函数功能：去掉文件名，返回目录
    if not os.path.isdir(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))
    url = '%s://%s/%s' % (o.scheme, o.netloc, filename)

    with open(filepath, 'wb') as f:
        c = Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()
