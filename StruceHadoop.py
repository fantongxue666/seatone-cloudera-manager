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
    构建hadoop集群（表单模式）
    
    HDFS NameNode：文件系统存储元数据的节点 1个独立节点
    HDFS SecondaryNameNode：NameNode的影子节点 小规模集群可以和NameNode共享节点，大规模集群使用独立节点
    HDFS DataNode：HDFS数据存储 N个节点
    YARN ResourceManager：资源调度器 1个独立节点
    YARN NodeManager：是每一台机器框架的代理，是执行应用程序的容器，监控应用程序的资源使用情况并且向调度器ResourceManager汇报 N个节点（每台机器上都得有）
    注意点：NameNode、SecondaryNameNode、ResourceManager对资源的需求比较大，应该把他们三个分布到不同的机器上
    '''
    def hadoop_cluster_form(self,idList,typeList,userNameList,passWordList):
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

        try:
            index = 0
            while(index < len(idList)):
                if(typeList[index] == "NameNode"):
                    nameNodeIp = idList[index]
                    nameNodeUserName = userNameList[index]
                    nameNodePassWord = passWordList[index]
                elif(typeList[index] == "SecondaryNameNode"):
                    secondaryNameNodeIp = idList[index]
                    secondaryNameNodeUserName =  userNameList[index]
                    secondaryNameNodePassWord =  passWordList[index]
                elif(typeList[index] == "ResourceManager"):
                    resourceManagerIp = idList[index]
                    resourceManagerUserName = userNameList[index]
                    resourceManagerPassWord = passWordList[index]
                index = index + 1

            index = 0
            # 对每台机器进行执行脚本，搭建hadoop的基础环境
            resultList = []
            while(index < len(idList)):
                connection = SSHConnection(host_ip=idList[index], user_name=userNameList[index], password=passWordList[index], host_port=22)
                result = connection.execute_shell("hadoop-cluster.sh", logFilePath,nameNodeIp, secondaryNameNodeIp, resourceManagerIp,
                                         ','.join(idList),
                                         ','.join(typeList),
                                         ','.join(userNameList),
                                         ','.join(passWordList))
                connection.close()
                index = index + 1
                resultList.append(result)

            # 连接上NameNode节点 初始化NameNode节点 启动HDFS节点
            connection = SSHConnection(host_ip=nameNodeIp, user_name=nameNodeUserName, password=nameNodePassWord,host_port=22)
            connection.execute_command("hdfs namenode -format",logFilePath)
            connection.execute_command("source /etc/profile && /opt/module/hadoop-3.2.3/sbin/start-dfs.sh",logFilePath)

            # 连接上ResourceManager节点 启动YARN ResourceManager节点
            connection = SSHConnection(host_ip=resourceManagerIp, user_name=resourceManagerUserName,password=resourceManagerPassWord, host_port=22)
            connection.execute_command("source /etc/profile && /opt/module/hadoop-3.2.3/sbin/start-yarn.sh",logFilePath)
            print("================ Hadoop集群部署成功！ ========================")
            print("== Web 端查看 HDFS 的 NameNode：http://"+nameNodeIp+":9870        ==")
            print("== Web 端查看 YARN 的 ResourceManager：http://"+resourceManagerIp+":8088 ==")
            print("============================================================")
            if False in resultList:
                # 执行失败
                resultStr = 'ERROR'
            else:
                # 执行成功
                resultStr = 'SUCCESS'
            # 最后上传日志文件，并存储数据库文件预览地址
            sql = 'insert into mg_log(id,target_ip,log_url,log_type,log_status,log_time) values ("'+str(uuid.uuid4())+'","'+','.join(idList)+'","'+tempFileName+'","构建Hadoop集群","'+resultStr+'",now())'
            db = MysqlDB.DataBaseHandle()
            i = db.updateDB(sql)
            return True
        except Exception:
            return False

    '''
    构建hadoop集群（导入模式）
    '''

    def hadoop_cluster_import(self):
        # 当前文件的绝对路径
        BASE_DIR = os.path.dirname(__file__)
        # 读取cluster.xls
        list = self.read_excel(BASE_DIR + "/shell/hadoop-cluster.xls")



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
