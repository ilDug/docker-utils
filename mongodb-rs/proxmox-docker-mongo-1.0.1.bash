#!/bin/bash

########################################################################################
# creazione di un container con webserver NGINX PROXY MANAGER (reverse proxy)
# che esegue il DOCKER-ENGINE per ospitare ed esguire i docker-containers
# fondamentalmente un webserver dove possibile accedere ai containers per i test dei siti
#########################################################################################
#
# eseguire l'abilitazione del NESTING nelle opziopni del container per permettere 
# un ulteriore livello di virtualizzazione
#
# - Unprivileged container
# - template: Ubuntu 20.04
# - nelle opzioni del container → features → NESTING
#
#collegare alla cartella condivisa sul NAS 
        #   pct set 211 -mp0 /dag-pool/archive/Development/Server/Containers/proxmox-docker-mongo,mp=/app,shared=1
        #   pct set 211 --features nesting=1
        #   pct start 211 
        #   pct set 212 -mp0 /dag-pool/archive/Development/Server/Containers/proxmox-docker-mongo,mp=/app,shared=1
        #   pct set 212 --features nesting=1
        #   pct start 212 
        #   pct set 213 -mp0 /dag-pool/archive/Development/Server/Containers/proxmox-docker-mongo,mp=/app,shared=1
        #   pct set 213 --features nesting=1
        #   pct start 213 
#########################################################################################




# configurazione di Ubuntu
timedatectl set-timezone Europe/Rome


apt-get update
apt-get install -y \
  nfs-common \
  nfs-kernel-server \
  cifs-utils \
  vim \
  software-properties-common \
  curl


#modifica il file di configurazione di SSH per permettere il collemgamento dall'esterno
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
cat /etc/ssh/sshd_config
systemctl restart ssh.service 


# DOCKER installation (COME DA ISTRUZIONI DEL SITO DOCKER)

## SET UP THE REPOSITORY
apt-get remove docker docker-engine docker.io containerd runc
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

#Configure Docker to start on boot
systemctl enable docker.service
systemctl enable containerd.service

## INSTALL DOCKER COMPOSE
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose


chmod +x /usr/local/bin/docker-compose
docker-compose --version
