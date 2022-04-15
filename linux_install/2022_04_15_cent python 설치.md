## cent python3.8 설치

~~~bash
yum -y install gcc openssl-devel libffi-devel bzip2-devel 
wget https://python.org/ftp/python/3.8.2/Python-3.8.2.tgz 
cd /usr/local cp ~/Python-3.8.2.tgz . 
tar xzf Python-3.8.2.tgz 
cd Python-3.8.2/ 
./configure --enable-optimizations 

make altinstall 
vi ~/.bashrc​
``` # User specific aliases and functions 
alias python="/usr/local/bin/python3.8" ## 이 줄을 추가한다.
alias pip=pip3.8 
alias rm='rm -i' 
alias rm='cp -i' 
...​``` 
source ~/.bashrc 
python -V ## 버전을 확인해보자

~~~

