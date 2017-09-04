# coding = UTF-8

import redis

# 连接数据库
rcon = redis.Redis(host='106.14.237.43', port=6379, password='z1Yh2900')

# 返回数据库的个数
print(rcon.dbsize())

# 返回符合特征的键列表
print(rcon.keys('fo*'))

# delete(*names)
# exists(name)
# get(name)



