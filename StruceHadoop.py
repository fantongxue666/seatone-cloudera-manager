from SSHConnect import SSHConnection

'''
构建Hadoop服务
'''
class hadoopStruction:
    '''
    param：alone（单机） cluster（集群）
    '''
    def struct(self,ip,param,username,password,port=22):
        if(param == "alone"):
            print("开始构建hadoop单机版!")
            # 上传部署脚本 执行
            connection = SSHConnection(host_ip=ip, user_name=username, password=password, host_port=port)
            connection.execute_shell("hadoop.sh")
            connection.close()
        elif(param == "cluster"):
            print("开始构建hadoop集群版!")

        else:
            print("暂不支持！")
        print("搭建完成！去看效果吧！")
