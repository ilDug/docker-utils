#! bash
ID=120
HOSTNAME=ek-docker
PASSWORD=adsadsekdocker
MEMORY=1024
DISK=8
IP=192.168.1.180/24

pct create $(ID) /mnt/pve/qnap-backup/template/cache/ubuntu-20.04-standard_20.04-1_amd64.tar.gz \
    --arch amd64 \
    --ostype ubuntu \
    --storage local-zfs \
    --hostname $(HOSTNAME) \
    --password $(PASSWORD) \
    --cores 4  \
    --memory $(MEMORY) \
    --swap 0 \
    --rootfs local-zfs:$(DISK) \
    --net0 name=eth0,bridge=vmbr0,gw=192.168.1.1,ip=$(IP),firewall=1 \
    --nameserver 192.168.1.161 \
    --searchdomain eurokemical.lan \
    --features nesting=1 \
    --onboot 1 \
    --unprivileged 1 \


# MOUNT POINTS
pct set $(ID) -mp0 /mnt/qnap1/app,mp=/mnt/qnap1/app,shared=1,replicate=0 \

pct start $(ID)

# configurazione di Ubuntu TIMEZONE
pct exec $(ID) -- bash -c "timedatectl set-timezone Europe/Rome"
#modifica il file di configurazione di SSH per permettere il collemgamento dall'esterno
pct exec $(ID) -- bash -c "sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config"
pct exec $(ID) -- bash -c "systemctl restart ssh.service"
pct exec $(ID) -- bash -c "apt-get update && apt-get upgrade -y"
pct exec $(ID) -- bash -c "apt-get install -y  nfs-common  nfs-kernel-server  cifs-utils  vim  software-properties-common  curl  vsftpd"

pct exec $(ID) -- bash -c "echo $(PASSWORD) | passwd --stdin root"



# pct exec <id> -- bash -c "yum update -y &&\
    # yum install -y openssh-server &&\
    # systemctl start sshd &&\
    # useradd -mU hogeuser &&\
    # echo "password" | passwd --stdin hogeuser"