#!/bin/bash

function disable_firewalld(){
    echo "###Step 1: disable firewalld"
    systemctl stop firewalld
    systemctl disable firewalld
    echo ""
}

function disable_selinux(){
    echo "###Step 2: close selinux"
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
    echo ""
}

function enable_ip_forward(){
    echo "###Step 3: open linux ip_forward"
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
    sysctl -p
    echo ""
}

function checkout_yum_repo(){
    echo "###Step 4: modify yum.repo.d and checkout aliyun base repo"
    yum install wget
    cd /etc/yum.repos.d
    mkdir repo.bak
    mv /etc/yum.repos.d/*.repo repo.bak/
    wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo
    cd $HOME
    yum clean all && yum makecache
    yum update
    echo ""
}

function install_required_tools(){
    echo "###Step 5: yum install required tools"
    yum install vim
    yum install -y openssl-devel
    yum -y install sqlite-devel
    yum groupinstall -y "Development Tools"
    echo ""
}

function install_python(){
    echo "###Step 6: pyenv installer"
    curl https://pyenv.run | bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
    pyenv --version
    pyenv install 3.6.8
    pyenv global 3.6.8
    python -m pip install --upgrade pip
    echo ""
}

function install_golang(){
    echo "###Step 7: gvm installer"
    yum install -y git make bison gcc glibc-devel
    bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
    source ~/.bashrc
    gvm install go1.4 -B
    gvm use go1.4
    gvm install go1.19
    gvm use go1.19
    echo ""
}

function install_nodejs(){
    echo "###Step 8: install nodejs >= v10.0"
    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
    source ~/.bashrc
    nvm install 14
    nvm use 14
    node -v
    npm -v
    echo ""
}

function install_docker() {
    echo "###Step 9: install latest docker"
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
    yum install docker-ce docker-ce-cli containerd.io
    yum install docker-ce- docker-ce-cli- containerd.io
    systemctl start docker
    systemctl enable docker
    echo ""
}

function start_docker_mysql() {
    echo "###Step 10: install mysql with docker"
    mkdir /opt/mysql/data -p
    docker pull mysql
    docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -v /opt/mysql/data/:/var/lib/mysql -d mysql
    docker container update --restart=always mysql
    echo ""
}

function start_docker_postgresql() {
    echo "###Step 11: install postgresql with docker"
    mkdir /opt/postgresql/data -p
    docker pull postgres
    docker run -d -p 5432:5432 --name=postgresql -v /opt/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=root postgresql
    docker container update --restart=always postgresql
    echo ""
}

redis_conf="
# bind 192.168.1.100 10.0.0.1
# bind 127.0.0.1 ::1
#bind 127.0.0.1


protected-mode no
port 6379
tcp-backlog 511
requirepass 000415
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile ""
databases 30
always-show-logo yes
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-disable-tcp-nodelay no
replica-priority 100
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
appendonly yes
appendfilename "appendonly.aof"
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-max-len 128
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes"

function start_docker_redis() {
    echo "###Step 12: install redis with docker"
    mkdir /opt/redis/etc -p
    echo $redis_conf > /opt/redis/etc/redis.conf
    mkdir /opt/redis/data -p
    docker pull redis
    docker run --restart=always --log-opt max-size=100m --log-opt max-file=2 -p 6379:6379 --name redis -v /opt/redis/etc/redis.conf:/etc/redis/redis.conf -v /opt/redis/data:/data -d redis redis-server /etc/redis/redis.conf  --appendonly yes  --requirepass root
    docker container update --restart=always redis
    echo ""
}

disable_firewalld
disable_selinux
enable_ip_forward
checkout_yum_repo
install_required_tools
install_python
install_golang
install_nodejs
install_docker
start_docker_mysql
start_docker_postgresql
start_docker_redis
reboot