# 作者：xiaozhang
# 日期：2019/8/28 11:44
# 工具：PyCharm Python版本：3.6

import requests
import random

# 不同浏览器的UA
header_list = [
    # 遨游
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
    # 火狐
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
    # 谷歌
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
]

headers = random.choice(header_list)
PROXY_POOL_URL="http://127.0.0.1:5555/random"

url_http = "http://httpbin.org/get"

def get_proxy():
    try:
        response = requests.get(url=PROXY_POOL_URL)
        if response.status_code==200:
            return response.text
    except  Exception as e:
        return None

proxy=get_proxy()
if proxy:
    print(proxy)
    proxies={
        "http":proxy,
        "https":proxy
    }
    try:
        response=requests.get(url=url_http,headers=headers,timeout=7,proxies=proxies).json()
        print(response)
    except Exception as e:
        print(e)

# 随机获取UA和代理IP
# # response=requests.get(url=url_https,headers=headers,proxies=proxies_https,timeout=5).json()
