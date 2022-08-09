from StruceHadoop import hadoopStruction

print("#####################################")
print("##         ClouderaManager         ##")
print("#####################################")

print("1 Hadoop")
print("2 Flink")
print("3 Spark")
print("4 Redis")
str = input("请选择要构建的服务:")
if(str == "1"):
    hadoopStruction().struct()
else:
    print("暂不支持此服务！")
