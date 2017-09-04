#coding:utf8
import paramiko
import os
class Paramiko:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None
    def connect(self,host,user,pwd=None,port=22,key=None):
        try:
            self.host = host
            if pwd is None: #私钥连接
                if key is None:
                    key = paramiko.RSAKey.from_private_key_file('id_rsa')
                    self.ssh.connect(host,port,user,pkey=key)
                else:
                    self.ssh.connect(host, port, user, pkey=key)

            else: #密码连接
                self.ssh.connect(host,port,user,pwd)
        except Exception,e:
            print str(e)

    # 执行命令
    def cmd(self,cmd):
        try:
            print '-' * 50 + self.host + '：' + cmd + '-' * 50
            stdin,stdout,stderr = self.ssh.exec_command(cmd)
            for line in stdout:
                print line,

            # 等待命令执行完毕，否则阻塞
            # channel = stdout.channel  # 通道
            # status = channel.recv_exit_status()  # 等待shell关闭以后 进程继续执行、否则阻塞
            # print status

        except Exception,e:
            print str(e)

    # 获取sftp对象
    def __get_sftp(self):
        # 没有sftp则创建
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())  # 获取ssh连接 然后创建sftp管道
        return self.sftp

    # 远程文件上传
    def upload(self,local,remote):
        try:
            sftp = self.__get_sftp() #获取sftp
            res = sftp.put(local,remote) # 上传文件
        except Exception,e:
            print str(e)

    #远程文件下载
    def download(self,remote,local):
        try:
            sftp = self.__get_sftp() #获取sftp
            res = sftp.get(remote,local) # 上传文件
        except Exception,e:
            print str(e)

Base_dir = os.path.dirname(os.path.dirname(__file__)) #项目根路径