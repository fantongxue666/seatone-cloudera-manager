from SSHConnect import SSHConnection

'''
构建Hadoop服务
'''
class hadoopStruction:
    '''
    param：alone（单机） cluster（集群）
    '''
    def struct(self,ip,param,username,password):
        if(param == "alone"):
            print("开始构建hadoop单机版!")
            # 测试连接执行
            connection = SSHConnection(host_ip='192.168.195.128', user_name='root', password='aini12345', host_port='22')
            connection.execute_shell("hadoop.sh")
        elif(param == "cluster"):
            print("开始构建hadoop集群版!")
        else:
            print("暂不支持！")
        print("搭建完成！去看效果吧！")
