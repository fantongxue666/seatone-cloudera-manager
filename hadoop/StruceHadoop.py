from utils.SSHConnect import SSHConnection

'''
构建Hadoop服务
'''
class hadoopStruction:

    '''
    构建hadoop单机版
    '''
    def hadoop_alone(self,ip,username,passwd):
        # 上传部署脚本 执行
        connection = SSHConnection(host_ip=ip, user_name=username, password=passwd, host_port=22)
        connection.execute_shell("hadoop-alone.sh")
        connection.close()


    '''
    构建hadoop集群
    '''
    def hadoop_cluster(self,dict):

        pass