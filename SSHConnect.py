import paramiko

class SSHConnection:
    '''
    初始化
    '''
    def __init__(self, host_ip, host_port, user_name, password):
        self.host_ip = host_ip
        self.host_port = host_port
        self.user_name = user_name
        self.password = password
        # SSH远程连接
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host_ip, host_port, user_name, password)

    '''
    执行ssh命令
    '''
    def execute_command(self,command):
        test = self.host_ip
        stdin, stdout, stderr = self.ssh.exec_command(command)
        out = stdout.readlines()
        err = stderr.readlines()
        #关闭连接
        self.ssh.close()
        return out,err

    '''
    执行shell脚本
    '''
    def execute_shell(self,shellAbsolutePath):
        connection = self.ssh
        ftp = connection.open_sftp()
        # 把shell脚本上传至指定目录
        pass



'''
测试连接执行
connection = SSHConnection(host_ip='192.168.1.230', user_name='root', password='bigdata123', host_port='22')
out,error = connection.execute_command("ifconfig;")
print(out)
print(error)
'''
