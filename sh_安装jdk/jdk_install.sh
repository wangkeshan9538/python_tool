#!/bin/bash


 
sudo yum  install -y java-1.8.0-openjdk-devel.x86_64
sudo touch /etc/profile.d/java_path.sh

sudo sh -c "echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.171-8.b10.el6_9.x86_64
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$PATH:$JAVA_HOME/bin' > /etc/profile.d/java_path.sh"

source /etc/profile

 which java >/dev/null
if [ $? -eq 0  ] 
then echo '安装完成'
else echo '安装失败'
fi  