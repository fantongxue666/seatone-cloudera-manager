#!/usr/bin/bash
#
# 执行此文件的命令：source hadoop.sh 参数1 参数2 参数3
# 参数1：服务器IP地址
# 参数2：登录用户名
# 参数3：登录密码
#
echo "检查是否存在yum工具..."
yum_result=$(yum --version)
if [ $? -ne 0 ];then
	echo "不存在yum工具，开始安装yum..."
fi
expect=$(expect -v)
if [ $? -ne 0 ];then
	echo "不存在expect工具，开始安装expect..."
	`yum install -y expect`
fi
echo "检查是否存在JDK环境..."
java -version
if [ $? -ne 0 ] || [ -z "$(echo $JAVA_HOME)" ];then
        echo "删除openssh自带的JDK..."
        for every in `rpm -qa | grep jdk`
        do
                rpm -e --nodeps $every
        done
        echo "下载jdk8..."
	cd /tmp && wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" https://repo.huaweicloud.com/java/jdk/8u151-b12/jdk-8u151-linux-x64.rpm
	chmod +x /tmp/jdk-8u151-linux-x64.rpm && rpm -ivh /tmp/jdk-8u151-linux-x64.rpm
	echo "配置JDK环境变量..."
	sed -i '$aexport JAVA_HOME=/usr/java/jdk1.8.0_151' /etc/profile
	sed -i '$aexport PATH=$JAVA_HOME/bin:$PATH' /etc/profile
	source /etc/profile
	test_result=$(java -version)
	if [ $? -eq 0 ];then
		echo "jdk安装成功！"
		rm -rf /tmp/jdk-8u151-linux-x64.rpm
	else
		echo "ERROR！jdk安装失败！"
		exit
	fi
else
	echo "存在JDK环境!"
fi
echo "检查是否存在hadoop环境..."
hadoop version
if [ $? -ne 0 ];then
	echo "不存在hadoop环境，下载hadoop安装包..."
	cd /tmp && wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz
	if [ ! -d /opt/module ];then
		mkdir -p /opt/module
	fi
	cd /tmp && tar -zxvf hadoop-3.2.3.tar.gz -C /opt/module
	if [ -n "$(ls /opt/module | grep hadoop-3.2.3)" ];then
		echo "解压成功!"
	else
		echo "ERROR！解压失败！"
		exit
	fi
	JAVA_HOME=$(echo $JAVA_HOME)
	echo "配置hadoop环境变量..."
        sed -i '$aexport HADOOP_HOME=/opt/module/hadoop-3.2.3' /etc/profile
        sed -i '$aexport PATH=$HADOOP_HOME/bin:$PATH' /etc/profile
        sed -i '$aexport PATH=$HADOOP_HOME/sbin:$PATH' /etc/profile
	sed -i '$aexport HDFS_NAMENODE_USER=root' /etc/profile
	sed -i '$aexport HDFS_DATANODE_USER=root' /etc/profile
	sed -i '$aexport HDFS_SECONDARYNAMENODE_USER=root' /etc/profile
	sed -i '$aexport YARN_RESOURCEMANAGER_USER=root' /etc/profile
	sed -i '$aexport YARN_NODEMANAGER_USER=root' /etc/profile
        source /etc/profile
	eval sed -i '$aexport JAVA_HOME=${JAVA_HOME}' /opt/module/hadoop-3.2.3/etc/hadoop/hadoop-env.sh
        test_result=$(hadoop version)
        if [ $? -eq 0 ];then
        	echo "Hadoop安装成功！"
		#rm -rf /tmp/hadoop-3.2.3.tar.gz
        else
        	echo "ERROR！Hadoop安装失败！"
        	exit
        fi
fi
export JAVA_HOME=$JAVA_HOME
export HADOOP_HOME=/opt/module/hadoop-3.2.3
export PATH=$HADOOP_HOME/bin:$PATH
export PATH=$HADOOP_HOME/sbin:$PATH
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root

echo "关闭防火墙..."
`systemctl stop firewalld`
echo "自动配置hadoop的自定义配置..."
sed -i '19a<property><name>fs.defaultFS</name><value>hdfs://0.0.0.0:8020</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/core-site.xml
sed -i '20a<property><name>hadoop.tmp.dir</name><value>/opt/module/hadoop-3.2.3/data</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/core-site.xml
sed -i '21a<property><name>hadoop.http.staticuser.user</name><value>root</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/core-site.xml
sed -i '22a<property><name>hadoop.proxyuser.root.hosts</name><value>*</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/core-site.xml
sed -i '23a<property><name>hadoop.proxyuser.root.groups</name><value>*</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/core-site.xml
sed -i '19a<property><name>dfs.namenode.http-address</name><value>0.0.0.0:9870</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/hdfs-site.xml
sed -i '20a<property><name>dfs.namenode.secondary.http-address</name><value>0.0.0.0:9868</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/hdfs-site.xml
sed -i '15a<property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/yarn-site.xml
sed -i '16a<property><name>yarn.resourcemanager.hostname</name><value>0.0.0.0</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/yarn-site.xml
sed -i '19a<property><name>mapreduce.framework.name</name><value>yarn</value></property>' /opt/module/hadoop-3.2.3/etc/hadoop/mapred-site.xml

echo "配置免密登录..."
if [ -z "$(ls ~/.ssh|grep id_rsa.pub)" ];then
	expect << EOF
		spawn ssh-keygen -t rsa
		expect {
			"id_rsa):" { send "\n";exp_continue }
			"passphrase):" { send "\n";exp_continue }
			"again:" { send "\n";exp_continue }
		}
EOF
fi
if [ -z "$(ls ~/.ssh|grep id_rsa.pub)" ];then
	echo "ERROR！配置免密登录有问题，没有配置成功！"
	exit
else
	cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
fi

echo "开始启动hadoop各项服务..."
/opt/module/hadoop-3.2.3/sbin/start-all.sh
echo "hdfs初始化..."
hdfs namenode -format
echo "======================================================"
echo "Web 端查看 HDFS 的 NameNode：http://0.0.0.0:9870"
echo "Web 端查看 YARN 的 ResourceManager：http://0.0.0.0:8088"
echo "======================================================"


