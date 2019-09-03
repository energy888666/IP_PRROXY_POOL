# 作者：xiaozhang
# 日期：2019/9/2 16:52
# 工具：PyCharm Python版本：3.6
import redis
from proxypool.setting import  REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY

host=REDIS_HOST
port=REDIS_PORT
password=REDIS_PASSWORD

db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True) #decode_responses=True目的是为了显示中文
# print(db.zrevrange(REDIS_KEY, 0, 100))
print(db.zrangebyscore(REDIS_KEY, 100, 100)[0])