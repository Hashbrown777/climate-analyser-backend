if [ "$(id -u)" != "0" ]; then
echo "This script must be run as root through sudo." 1>&2
exit 1
fi
RUNASUSER="sudo -u $SUDO_USER"

cp slurm.conf /usr/local/etc/slurm.conf
yum -y install munge
chown ec2-user /etc/munge
chown ec2-user /var/lib/munge
chown ec2-user /var/log/munge
chown ec2-user /var/run/munge
mkdir /var/run/munge
chown ec2-user /var/run/munge
dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key
chown ec2-user /etc/munge/munge.key
chmod 700 /etc/munge/munge.key

mkdir Slurm
cd Slurm
curl http://www.schedmd.com/download/latest/slurm-14.03.7.tar.bz2 -o slurm-14.03.7.tar.bz2
tar --bzip -x -f slurm*tar.bz2
cd slurm-14.03.7
./configure
make
make install

mkdir /slurm
mkdir /slurm/slurmd

