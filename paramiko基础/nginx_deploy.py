#coding:utf8
from base import Paramiko
import config

def nginx_deploy():
    for host in config.webserver:
        p = Paramiko()
        #密码方式连接
        # p.connect(host=host[0],user=host[1],pwd=host[2])
        # p.upload('id_rsa.pub','/root/.ssh/id_rsa.pub')
        # p.cmd('cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys')

        # #私钥方式连接
        p.connect(host=host[0],user=host[1])
        p.cmd('ls')

if __name__ == '__main__':
    nginx_deploy()