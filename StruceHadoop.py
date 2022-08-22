import time
import uuid

from flask import jsonify

import MysqlDB
from SSHConnect import SSHConnection
import os
import xlrd

'''
构建Hadoop服务
'''


class hadoopStruction:
    '''
    构建hadoop单机版
    '''

    def hadoop_alone(self, ip, username, passwd):

        # 创建日志文件
        BASE_DIR = os.path.dirname(__file__)
        tempDir = BASE_DIR + "/shell/logs/"
        if not os.path.exists(tempDir):
            os.mkdir(tempDir)
        tempFileName = str(uuid.uuid4()) + ".txt"
        logFilePath = tempDir + tempFileName
        # 日志文件不存在就创建
        try:
            f = open(logFilePath, 'r')
            f.close()
        except IOError:
            f = open(logFilePath, 'w')
            f.close()

        # 上传部署脚本 执行
        connection = SSHConnection(host_ip=ip, user_name=username, password=passwd, host_port=22)
        result = connection.execute_shell(shellName="hadoop-alone.sh", logFilePath=logFilePath)
        connection.close()
        if(result == True):
            resultStr = 'SUCCESS'
        else:
            resultStr = 'ERROR'

        # 最后上传日志文件，并存储数据库文件预览地址
        sql = 'insert into mg_log(id,target_ip,log_url,log_type,log_status,log_time) values ("'+str(uuid.uuid4())+'","'+ip+'","'+tempFileName+'","构建Hadoop单机版","'+resultStr+'",now())'
        db = MysqlDB.DataBaseHandle()
        i = db.updateDB(sql)


    '''
    构建hadoop集群
    
    HDFS NameNode：文件系统存储元数据的节点 1个独立节点
    HDFS SecondaryNameNode：NameNode的影子节点 小规模集群可以和NameNode共享节点，大规模集群使用独立节点
    HDFS DataNode：HDFS数据存储 N个节点
    YARN ResourceManager：资源调度器 1个独立节点
    YARN NodeManager：是每一台机器框架的代理，是执行应用程序的容器，监控应用程序的资源使用情况并且向调度器ResourceManager汇报 N个节点（每台机器上都得有）
    
    注意点：NameNode、SecondaryNameNode、ResourceManager对资源的需求比较大，应该把他们三个分布到不同的机器上
    '''

    def hadoop_cluster(self):
        # 当前文件的绝对路径
        BASE_DIR = os.path.dirname(__file__)
        # 读取cluster.xls
        list = self.read_excel(BASE_DIR + "/shell/hadoop-cluster.xls")
        # IP列表
        ip_list = []
        nameNodeIp = ""
        secondaryNameNodeIp = ""
        resourceManagerIp = ""
        for computer in list:
            if (computer[0] == "NameNode"):
                nameNodeIp = computer[1]
            if (computer[0] == "SecondaryNameNode"):
                secondaryNameNodeIp = computer[1]
            if (computer[0] == "ResourceManager"):
                resourceManagerIp = computer[1]

            if computer[1] in ip_list:
                pass
            else:
                ip_list.append(computer[1])
        # 对每台机器进行执行脚本，搭建hadoop的基础环境
        for computer in list:
            connection = SSHConnection(host_ip=computer[1], user_name=computer[2], password=computer[3], host_port=22)
            # 参数： 三个主节点的ip 顺序（NameNode,SecondaryNameNode,ResourceManager）
            connection.execute_shell("hadoop-cluster.sh", nameNodeIp, secondaryNameNodeIp, resourceManagerIp,
                                     ','.join(ip_list))
            connection.close()

        # 对每台机器进行执行脚本，配置互信功能，免密登录
        # TODO 所有机器的用户名和密码暂时设置成一样的，暂时全部写死为 root bigdata123，后期解决这个问题
        for computer in list:
            if (computer[0] == "NameNode"):
                NameNode_userName = computer[2]
                NameNode_passWord = computer[3]
            elif (computer[0] == "ResourceManager"):
                ResourceManager_userName = computer[2]
                ResourceManager_passWord = computer[3]

        # 连接上NameNode节点
        connection = SSHConnection(host_ip=nameNodeIp, user_name=NameNode_userName, password=NameNode_passWord,
                                   host_port=22)
        connection.execute_shell("hadoop-cluster-ssh-trust.sh", ','.join(ip_list))
        # 初始化NameNode节点
        connection.execute_command("hdfs namenode -format")
        # 启动HDFS节点
        connection.execute_command("source /etc/profile && /opt/module/hadoop-3.2.3/sbin/start-dfs.sh")

        # 连接上ResourceManager节点
        connection = SSHConnection(host_ip=resourceManagerIp, user_name=ResourceManager_userName,
                                   password=ResourceManager_passWord, host_port=22)
        # 启动YARN ResourceManager节点
        connection.execute_command("source /etc/profile && /opt/module/hadoop-3.2.3/sbin/start-yarn.sh")
        print("================ Hadoop集群部署成功！ ========================")
        print("== Web 端查看 HDFS 的 NameNode：http://0.0.0.0:9870        ==")
        print("== Web 端查看 YARN 的 ResourceManager：http://0.0.0.0:8088 ==")
        print("============================================================")

    '''
    读取excel文件
    列表的方式实现 [ [用例编号,用例名称],[],[] ]   外部一个列表元素一个用例  内部列表就是用例详情
    '''

    def read_excel(self, excel_path):
        workbook = xlrd.open_workbook(excel_path)  # 打开excel工作簿
        sheet = workbook.sheet_by_index(0)  # 选择工作表
        case_infos = []
        rows = sheet.nrows  # 确定行数
        cols = sheet.ncols  # 确定列数
        for i in range(1, rows):
            case_info = []
            for j in range(0, cols):
                case_info.append(sheet.cell_value(i, j))
            case_infos.append(case_info)
        return case_infos
