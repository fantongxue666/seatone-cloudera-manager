#!/usr/bin/bash

echo "检测expect工具是否存在..."
expect=$(expect -v)
if [ $? -ne 0 ]; then
  	echo "不存在expect工具，开始安装expect..."
  	$(yum install -y expect)
fi
echo "配置集群所有机器的免密登录..."

str=$1
oldIFS=$IFS
IFS=,
arr=($str)
# 循环N台机器的IP地址，生成密钥文件authorized_keys
for ip in ${arr[*]}; do
	expect <<EOF
     ssh root@$ip
     expect{
      "yes/no" { send "yes\r";exp_continue }
      "password:"{ send "bigdata123\r";exp_continue }
    }
    spawn ssh-keygen -t rsa &>/dev/null
    expect {
      "id_rsa):" { send "\n";exp_continue }
      "passphrase):" { send "\n";exp_continue }
      "again:" { send "\n";exp_continue }
    }
    cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys &> /dev/null
    exit
    if [ !-f ~/.ssh/authorized_keys ];then
       touch ~/.ssh/authorized_keys
    fi
    ssh root@$ip cat ~/.ssh/authorized_keys >> ~/.ssh/authorized_keys  &> /dev/null
     expect{
      "yes/no" { send "yes\r";exp_continue }
      "password:"{ send "bigdata123\r";exp_continue }
    }

EOF
done
# 循环N台机器的IP地址，scp拷贝key文件到其他机器
for ip in ${arr[*]}; do
	expect <<EOF
    scp -R ~/.ssh/authorized_keys root@$ip:~/.ssh/
        expect{
            "yes/no" { send "yes\r";exp_continue }
            "password:"{ send "bigdata123\r";exp_continue }
       }

EOF
done
