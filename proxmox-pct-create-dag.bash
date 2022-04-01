#!/bin/bash

########################################################################################
# creazione di un container 
# che esegue il DOCKER-ENGINE per ospitare ed esguire i docker-containers
#########################################################################################
#
# eseguire l'abilitazione del NESTING nelle opziopni del container per permettere 
# un ulteriore livello di virtualizzazione
#
# - Unprivileged container
# - template: Ubuntu 20.04
# - nelle opzioni del container → features → NESTING
#########################################################################################


#! bash
ID=251
HOSTNAME=docker-nginx
PASSWORD=adsadsdocker
MEMORY=1024
DISK=8
IP=10.0.0.251/24

#creazione del container proxmox
ppct create $ID /var/lib/vz/template/cache/ubuntu-20.04-standard_20.04-1_amd64.tar.gz \
    --arch amd64 \
    --ostype ubuntu \
    --storage local-lvm \
    --hostname $HOSTNAME \
    --password $PASSWORD \
    --cores 4  \
    --memory $MEMORY \
    --swap 0 \
    --rootfs local-lvm:$DISK \
    --net0 name=eth0,bridge=vmbr0,gw=10.0.0.1,ip=$IP,firewall=1 \
    --nameserver 10.0.0.101 \
    --searchdomain dag.lan \
    --features nesting=1 \
    --onboot 1 \
    --unprivileged 1 \

# MOUNT POINTS
pct set $ID -mp0 /dag-pool/archive/,mp=/mnt/archive,shared=1,replicate=0 
pct set $ID -mp1 /dag-pool/proxmox/containers/docker-nginx,mp=/apps,shared=1,replicate=0 

pct start $ID

# configurazione di Ubuntu TIMEZONE
pct exec $ID -- bash -c "timedatectl set-timezone Europe/Rome"

#modifica il file di configurazione di SSH per permettere il collemgamento dall'esterno
pct exec $ID -- bash -c "sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config"
pct exec $ID -- bash -c "systemctl restart ssh.service"
pct exec $ID -- bash -c "apt-get update && apt-get upgrade -y"
pct exec $ID -- bash -c "apt-get install -y  nfs-common  nfs-kernel-server  cifs-utils  vim  software-properties-common  curl  vsftpd"

pct exec $ID -- bash -c "passwd root"
# pct exec $ID -- bash -c "echo $PASSWORD | passwd --stdin root"
# pct exec $ID -- bash -c 'echo "root:${PASSWORD}" | sudo chpasswd'
