#!/bin/sh

#please use: wget https://*/*.sh && bash *.sh



yum -y install sudo git tar wget

#scp -r /Users/zychen/code/zhisearch_linux root@*:/home

yum -y install anaconda

cd /home

wget https://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh

bash Anaconda3-4.3.0-Linux-x86_64.sh

#echo "PATH=/root/anaconda3/bin" > /root/.bashrc

bash ~/.bashrc

PATH=/root/anaconda3/bin

python /home/zhisearch_linux/web/main_web.py
