import requests

r = requests.get('http://httpbin.org/get')
print(r.status_code, r.reason)
print(r.text)

r = requests.get('http://httpbin.org/get',
                 params={'a': '5', 'b': '9'})
print(r.json())

# 自定义headers请求
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
headers = {'User-Agent': ua}
r = requests.get('http://httpbin.org/headers',
                 headers=headers)
print(r.json())


r = requests.post('http://httpbin.org/post',
                  data={'a': '1'})
print(r.json())

# 带cookies的请求
cookies = dict(userid='123', token='xxxxxxxxxxxxx')
r = requests.get('http://httpbin.org/cookies',
                 cookies=cookies)
print(r.json())

# Basic-auth认证请求
r = requests.get('http://httpbin.org/basic-auth/shi/123', auth=('shi', '123'))
print(r.json())

# 主动抛出状态码异常
# bad_r = requests.get('http://httpbin.org/status/404')
# bad_r.raise_for_status()

# 使用requests.Session()对象发出请求
s = requests.Session()

# session对象会保存服务器返回的set-cookies头信息里面的内容
s.get('http://httpbin.org/cookies/set/userid/123456')
s.get('http://httpbin.org/cookies/set/token/ttttttttttttt')

# 下一次请求会将本地所有的cookies信息自动添加到请求头信息里发送给服务器
r = s.get('http://httpbin.org/cookies')
print(r.json())

r = requests.get('http://httpbin.org/delay/3', timeout=5)
