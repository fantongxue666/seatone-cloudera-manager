from StruceHadoop import hadoopStruction
import os


def handle():
    print("#####################################")
    print("##         ClouderaManager         ##")
    print("#####################################")

    print("1 Hadoop")
    print("2 Flink")
    print("3 Spark")
    print("4 Redis")
    str = input("请选择要构建的服务：")
    if (str == "1"):
        print("1 单机版")
        print("2 集群版")
        str = input("请选择Hadoop的模式：")
        if (str == "1"):
            # 单机
            ip = input("请输入即将部署服务的服务器IP地址：")
            result = os.system('ping ' + ip)
            if (result == 0):
                userName = input("用户名：")
                passWord = input("密码：")
                hadoopStruction().struct(param="alone", ip=ip, username=userName, password=passWord)
            else:
                print("ERROR! 服务器不可用，请重新输入!")
        elif (str == "2"):
            # 集群
            ips = input("请输入集群服务器的IP列表（多个逗号隔开）：")
            try:
                ip_list = ips.split(",")
            except Exception:
                print("ERROR! 非法字符！")
            for temp_ip in ip_list:
                pass

        else:
            print("暂不支持！")
    else:
        print("暂不支持此服务！")


while (True):
    handle()
