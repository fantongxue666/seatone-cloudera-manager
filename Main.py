from StruceHadoop import hadoopStruction

'''
构建hadoop单机版
'''
def hadoop_alone():
    hadoopStruction().hadoop_alone(ip="192.168.195.128",username="root",passwd="aini12345")


'''
构建hadoop集群
'''
def hadoop_cluster():
    hadoopStruction().hadoop_cluster()



hadoop_cluster()