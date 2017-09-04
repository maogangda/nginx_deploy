#coding:utf8
from config.base import Paramiko
from config import host_config
import config
import paramiko
import os
import threading
import time

# 单进程
# def nginx_deploy(hosts):
#     for host in hosts:
#         p = Paramiko()
#
#         # Base_dir = os.path.dirname(os.path.abspath(os.getcwd()))
#         # print os.getcwd()
#         # print os.path.join(Base_dir, 'config', 'id_rsa')
#         key = paramiko.RSAKey.from_private_key_file(os.path.join(config.base.Base_dir,'config','id_rsa'))
#
#         p.connect(host=host[0],user=host[1],key=key) #建立连接
#         p.upload(os.path.join(config.base.Base_dir,'nginx_deploy','nginx.zip'),'/opt/nginx.zip')
#         p.cmd('unzip -o -d /opt /opt/nginx.zip')
#         p.cmd('python /opt/nginx_deploy.py')
#         p.cmd(r"sed -i '116 s%^%    include /usr/local/nginx1.10.2/conf/vhosts.d/*.conf;\n%' /usr/local/nginx1.10.2/conf/nginx.conf")
#         p.cmd('mkdir /usr/local/nginx1.10.2/conf/vhosts.d')
#         p.cmd('nginx -s reload')


# 多线程
# 创建所有主机连接
def get_ssh_client(hosts):
     key = paramiko.RSAKey.from_private_key_file(os.path.join(config.base.Base_dir, 'config', 'id_rsa'))
     clients = [] #所有主机连接列表
     for host in hosts:
         client = Paramiko()
         client.connect(host=host[0],user=host[1],key=key) #建立连接
         clients.append(client)
     return clients

#创建线程集合
def get_threads(clients):
    thread_list = []
    for client in clients: #循环所有连接
        thread = threading.Thread(target=nginx_cmd,args=(client,))
        thread_list.append(thread)
    return thread_list

#线程需要完成的任务
def nginx_cmd(client):
    client.upload(os.path.join(config.base.Base_dir, 'nginx_deploy', 'nginx.zip'), '/opt/nginx.zip')
    client.cmd('unzip -o -d /opt /opt/nginx.zip')
    client.cmd('python /opt/nginx_deploy.py')
    client.cmd(r"sed -i '116 s%^%    include /usr/local/nginx1.10.2/conf/vhosts.d/*.conf;\n%' /usr/local/nginx1.10.2/conf/nginx.conf")
    client.cmd('mkdir /usr/local/nginx1.10.2/conf/vhosts.d')
    client.cmd('nginx -s reload')

#开启线程
def nginx_deploy(thread_list):
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    # nginx_deploy(host_config.webserver) 单进程

    # 多线程部署nginx

    start = time.time()
    clients = get_ssh_client(host_config.webserver)
    thread_list = get_threads(clients)
    nginx_deploy(thread_list)
    end = time.time()
    print '---------------' + str(start - end) + '------------------'