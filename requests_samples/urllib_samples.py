import json
import urllib.request

# 返回response对象
r = urllib.request.urlopen('http://httpbin.org/get')
print(type(r))
# 返回字节数组
text = r.read()
print(text)
# 返回状态码和msg
# print(r.status, r.reason)

# 返回的内容是json字符串
textstr = text.decode('utf-8')
print(textstr)

# 返回的内容是json对象---也就是json字典
obj = json.loads(text)
print(obj)

# r.headers是一个HTTPMessage对象
# print(r.headers)
for k, v in r.headers._headers:
    print('%s: %s' % (k, v))
r.close()

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
req = urllib.request.Request('http://httpbin.org/user-agent')

# 添加自定义头信息
req.add_header('User-Agent', ua)

# 接收urllib.request.Request对象作为参数
r = urllib.request.urlopen(req)

resp = json.load(r)
# 取出字典对象的user-agent属性值
print('user-agent:', resp['user-agent'])
r.close()

auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='test',
                          uri='/basic-auth/shi/123',
                          user='shi',
                          passwd='123')
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
r = urllib.request.urlopen('http://httpbin.org')
print(r.read().decode('utf-8'))
r.close()

# 使用GET方法传递参数
params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 2})
url = 'http://httpbin.org/get?%s' % params
with urllib.request.urlopen(url) as f:
    print(json.load(f))

# 使用POST方法传递参数
data = urllib.parse.urlencode({'name': '小米', 'age': 2})
# 编码成字节数组
data = data.encode()
print(data)
with urllib.request.urlopen('http://httpbin.org/post', data) as f:
    print(json.load(f))

# 使用代理IP请求远程URL
# proxy_handler = urllib.request.ProxyHandler({
#                         # 代理服务器地址
#                         'http': 'http://iguye.com:41801'
#                     })
# # 需要验证代理用户名和密码时，使用ProxyBasicAuthHandler
# # proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
# opener = urllib.request.build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(r.read())

o = urllib.parse.urlparse('https://shi:123@httpbin.org/get?a=1&b=2#test')
print(o.netloc)
print(o.path)
print(o.query)
print(o.fragment)
print(o.geturl())
print(o.scheme)
print(list(o))
