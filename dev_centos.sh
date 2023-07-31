#!/bin/bash

function disable_firewalld(){
    echo "step 1: disable firewalld"
    systemctl stop firewalld
    systemctl disable firewalld
}

function disable_selinux(){
    echo "step 2: close selinux"
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
}

function enable_ip_forward(){
    echo "step 3: open linux ip_forward"
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
    sysctl -p
}

function checkout_yum_repo(){
    echo "step 4: modify yum.repo.d and checkout aliyun base repo"
    yum install wget
    cd /etc/yum.repos.d
    mkdir repo.bak
    mv /etc/yum.repos.d/*.repo repo.bak/
    wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo
    cd $HOME
    yum clean all && yum makecache
    yum update
}

function install_required_tools(){
    echo "step 5: yum install required tools"
    yum install vim
    yum groupinstall -y "Development Tools"
}

function install_python(){
    echo "step 6: pyenv installer"
    curl https://pyenv.run | bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
    pyenv --version
    pyenv install 3.6.8
    pyenv global 3.6.8
    python -m pip install --upgrade pip
}

function install_golang(){
    echo "step 7: gvm installer"
    yum install -y git make bison gcc glibc-devel
    bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
    source ~/.bashrc
    gvm install go1.4 -B
    gvm use go1.4
    gvm install go1.19
    gvm use go1.19
}

function install_nodejs(){
    echo "step 8: install nodejs >= v10.0"
    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
    source ~/.bashrc
    nvm install 14
    nvm use 14
    node -v
    npm -v
}

disable_firewalld
disable_selinux
enable_ip_forward
checkout_yum_repo
install_required_tools
install_python
install_golang
install_nodejs
reboot