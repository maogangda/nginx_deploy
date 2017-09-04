#coding:utf8
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('192.168.6.9',22,'root','123')
    dirs = '' #定义一个变量存储cd的路径
    while True:
        cmd = raw_input('>>')
        if cmd.startswith('cd '): #切换路径命令
            dirs = cmd + ';'
        elif cmd == 'exit':
            break
        else:
            stdin ,stdout,stderr = ssh.exec_command(dirs + cmd)
            for line in stdout:
                print line,
except Exception,e:
    print str(e)