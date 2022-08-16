#!/usr/bin/bash

echo "检查是否存在JDK环境...";
if [ -z $JAVA_HOME ];then
        echo "不存在JDK环境，删除openssh自带的JDK..."
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
	else
		echo "ERROR！jdk安装失败！"
	fi
	rm -rf /tmp/jdk-8u151-linux-x64.rpm
else
	echo "存在JDK环境!"
fi
echo "检查是否存在hadoop环境..."
if [ -z $HADOOP_HOME ];then
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
        test_result=$(hadoop version)
        if [ $? -eq 0 ];then
        	echo "Hadoop安装成功！"
		rm -rf /tmp/hadoop-3.2.3.tar.gz
        else
        	echo "ERROR！Hadoop安装失败！"
        	exit
        fi

	echo "自动配置hadoop的自定义配置..."
	echo "开始启动hadoop各项服务..."
	`systemctl stop firewalld`
	echo "配置免密登录..."
	`sh /opt/module/hadoop-3.2.3/sbin/start-all.sh`
fi

#echo "自动配置hadoop..."
#echo "开始启动hadoop各项服务..."
