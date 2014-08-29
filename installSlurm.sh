if [ "$(id -u)" != "0" ]; then
echo "This script must be run as root through sudo." 1>&2
exit 1
fi
RUNASUSER="sudo -u $SUDO_USER"

cp slurm.conf /etc/slurm/slurm.conf
yum -y install munge
chown root /etc/munge
chown root /var/lib/munge
chown root /var/log/munge
mkdir /var/run/munge
chown root /var/run/munge
dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key
chown root /etc/munge/munge.key
chmod 700 /etc/munge/munge.key

yum -y install readline-devel
yum -y install perl-devel
yum -y install munge-devel
yum -y install pam-devel
yum -y install perl-DBI
curl http://www.schedmd.com/download/latest/slurm-14.03.7.tar.bz2 -o slurm-14.03.7.tar.bz2
yum -y groupinstall "Development tools"
rpmbuild -ta slurm*.tar.bz2
rpm -i /root/rpmbuild/RPMS/x86_64/slurm-*

mkdir /slurm
chown ec2-user /slurm

