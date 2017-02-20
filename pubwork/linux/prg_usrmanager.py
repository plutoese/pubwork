# coding = UTF-8

import os

user = 'demo'
pwd = 'demo'
user_pwd = ':'.join([user,pwd])
print(user_pwd)

with open('/home/ubuntu/down/pwd.txt', 'w') as f:
    f.write(user_pwd)


os.system('sudo useradd -m -s /bin/bash {}'.format(user))
os.system('sudo chpasswd < /home/ubuntu/down/pwd.txt')