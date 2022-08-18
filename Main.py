from hadoop.StruceHadoop import hadoopStruction

'''
构建hadoop单机版
'''
def hadoop_alone():
    hadoopStruction().hadoop_alone(ip="192.168.195.128",username="root",passwd="aini12345")


'''
构建hadoop集群
'''
def hadoop_cluster():
    # 定义集群配置
    cluster_msg = {"NameNode":"192.168.195.128","DataNode":"192.168.195.128","NameNode":"192.168.1.101","SecondaryNameNode":"192.168.1.101",
                   "NodeManager":"192.168.195.128","NodeManager":"192.168.1.101"}
    hadoopStruction().hadoop_cluster(cluster_msg)



hadoop_alone()