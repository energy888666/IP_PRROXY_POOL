import json
import re
from .utils import get_page
from pyquery import PyQuery as pq
import requests

from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    #获取代理66
    def crawl_daili66(self, page_count=2):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling,代理66', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])
    #云代理
    def crawl_ip3366(self):
        '''
        获取云代理ip
        :return:
        '''
        for page in range(1, 2):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            print('Crawling云代理ip', start_url)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':'+ port
                yield result.replace(' ', '')

    #ip海代理
    def crawl_iphai(self):
        '''
        IP海
        :return:
        '''
        start_url = 'http://www.iphai.com/'
        print('Crawling,IP海', start_url)
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')
#无忧代理
    def crawl_data5u(self):

        '''
        无忧代理
        :return:
        '''
        url = 'http://www.data5u.com'
        print('Crawling,无忧代理', url)
        # requests的Session可以自动保持cookie,不需要自己维护cookie内容
        S = requests.Session()
        target_response = S.get(url=url, headers=headers)
        target_response.encoding = 'utf-8'
        data = etree.HTML(target_response.text)

        ip_info = data.xpath('//ul[@class="l2"]')
        for i in ip_info:
            # ip
            ip_addr = i.xpath('./span[1]/li[1]/text()')[0]
            # 协议类型
            # http_type = i.xpath('./span[4]/li[1]/text()')[0]
            # 提取出要处理的li标签的class属性里的大写字母
            port = "".join(i.xpath('./span[2]/li[1]/@class')).replace(r"port", "").strip()
            # 定义一个空列表用于保存找到字母的位置
            num = []
            # 遍历提取出来的字母，并对每一个遍历出来的字母在字符串"ABCDEFGHIZ"里找位置
            for j in port:
                num.append(str("ABCDEFGHIZ".find(j)))
            # 先把num连接成字符串，然后再转换为整型，最后处于8得到真正的端口
            ip_port = str(int(int("".join(num)) / 8))
            # 把处理好的ip地址和端口拼接到一起得到完整的ip地址和端口
            address_port = ip_addr + ":" + ip_port
            yield address_port.replace(' ', '')

    #快代理ip
    def rawl_kuaidaili(self):
        '''
        获取快代理ip
        :return:
        '''
        for i in range(1, 2):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            print('Crawling快代理ip', start_url)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')
    # 西祠代理,一般不能用
    def rawl_xicidaili(self):
        for i in range(1, 2):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            print('Crawling西祠代理ip', start_url)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    # def crawl_data5u(self):
    #     start_url = 'http://www.data5u.com/free/gngn/index.shtml'
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
    #         'Host': 'www.data5u.com',
    #         'Referer': 'http://www.data5u.com/free/index.shtml',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    #     }
    #     html = get_page(start_url, options=headers)
    #     if html:
    #         ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')

    # def crawl_ip3366(self):
    #     for i in range(1, 2):
    #         start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #             trs = find_tr.findall(html)
    #             for s in range(1, len(trs)):
    #                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #                 re_ip_address = find_ip.findall(trs[s])
    #                 find_port = re.compile('<td>(\d+)</td>')
    #                 re_port = find_port.findall(trs[s])
    #                 for address,port in zip(re_ip_address, re_port):
    #                     address_port = address+':'+port
    #                     yield address_port.replace(' ','')
    #