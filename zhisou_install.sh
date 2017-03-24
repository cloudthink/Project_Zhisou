#!/bin/sh

#please use: wget https://*/*.sh && bash *.sh
#cd ~/.ssh
#ssh-keygen -t rsa -C "824858863@qq.com"
#echo "added key in csdn?"
#git clone git@code.csdn.net:Datapad/zhisearch.git


yum -y install sudo git tar wget

#scp -r /Users/zychen/code/zhisearch_linux root@209.141.49.76:/home

yum -y install anaconda

cd /home

wget https://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh

bash Anaconda3-4.3.0-Linux-x86_64.sh

#echo "PATH=/root/anaconda3/bin" > /root/.bashrc

bash ~/.bashrc

PATH=/root/anaconda3/bin

python /home/zhisearch_linux/web/main_web.py