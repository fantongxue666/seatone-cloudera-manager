import paramiko
import uuid
import os
import shutil


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
    执行sh命令
    '''

    def execute_command(self, command, logFilePath):
        result = False
        test = self.host_ip
        stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=True)
        # 写入日志文件
        Note = open(logFilePath, mode='a',encoding='utf-8')
        # Note.writelines(stdout.readlines())
        # Note.close()
        while not stdout.channel.exit_status_ready():
            result = stdout.readline()
            new_result = result.replace("\n", "")
            print(new_result)
            Note.write(new_result)
            if(new_result.strip() == "###Over###"):
                # 操作成功的标志，记录状态
                result = True

            ###Over###
            # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
            if stdout.channel.exit_status_ready():
                a = stdout.readlines()
                for i in a:
                    result2 = i.replace("\n", "")
                    print(result2)
                    if(result2.strip() == "###Over###"):
                        # 操作成功的标志，记录状态
                        result = True
                    Note.write(result2.replace("\n", ""))
                break
        Note.close()
        return result

    '''
    执行shell脚本
    参数1：脚本名称 test.sh
    '''

    def execute_shell(self, shellName, logFilePath, *args):
        # 当前文件的绝对路径
        BASE_DIR = os.path.dirname(__file__)
        shellAbsolutePath = BASE_DIR + "/shell/" + shellName
        if not os.path.exists(shellAbsolutePath):
            print("error,file not exists!")
            return None
        # 把shell脚本上传至指定目录
        tempDir = BASE_DIR + "/shell/temp/"
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        tempFileName = str(uuid.uuid4()) + ".sh"
        newFilePath = tempDir + tempFileName
        # 存在就删除，复制shell为新的temp文件，用完再删除
        if os.path.exists(newFilePath):
            os.remove(newFilePath)
        # 复制
        shutil.copy(shellAbsolutePath, tempDir)
        # 重命名
        os.rename(tempDir + shellName, newFilePath)
        # tempShell上传至服务器
        connection = self.ssh
        ftp = connection.open_sftp()
        linuxPath = "/tmp/" + tempFileName
        ftp.put(newFilePath, linuxPath)
        ftp.close()
        # 删除临时文件
        os.remove(newFilePath)
        # 执行shell脚本
        count = len(args)
        command = "chmod +x " + linuxPath + " && source " + linuxPath;
        i = 1
        while i <= count:
            command = command + " " + args[i - 1]
            i = i + 1
        result = self.execute_command(command, logFilePath=logFilePath)
        # TODO 执行完删除linux上的临时shell 目前执行删除会报错，待解决
        # self.execute_command("sudo rm -rf /tmp/*.sh;")
        # return out,error
        return result

    def close(self):
        # 关闭连接
        self.ssh.close()
