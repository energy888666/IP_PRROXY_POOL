<<<<<<< HEAD

# ProxyPool

## 安装

### 安装Python

至少Python3.5以上

### 安装Redis

安装好之后将Redis服务开启

### 配置代理池

```
cd proxypool
```

=======
# IP_PRROXY_POOL
ProxyPool
安装
安装Python
至少Python3.5以上

安装Redis
安装好之后将Redis服务开启

配置代理池
cd proxypool
>>>>>>> bbd3858d0d87dbb8a9a0b66b79aeab44c3ffa4e0
进入proxypool目录，修改settings.py文件

PASSWORD为Redis密码，如果为空，则设置为None

<<<<<<< HEAD
#### 安装依赖

```
pip3 install -r requirements.txt
```

#### 打开代理池和API

```
python3 run.py
```

## 获取代理


利用requests获取方法如下

```python
=======
安装依赖
pip3 install -r requirements.txt
打开代理池和API
python3 run.py
获取代理
利用requests获取方法如下

>>>>>>> bbd3858d0d87dbb8a9a0b66b79aeab44c3ffa4e0
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
<<<<<<< HEAD
```
=======
>>>>>>> bbd3858d0d87dbb8a9a0b66b79aeab44c3ffa4e0
