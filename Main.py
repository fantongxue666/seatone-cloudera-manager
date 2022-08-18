from StruceHadoop import hadoopStruction
import os

'''
构建hadoop单机版
'''
def hadoop_alone():
    hadoopStruction().struct(param="alone", ip="192.168.195.128", username="root", password="aini12345")

hadoop_alone()