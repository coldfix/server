#! /bin/bash
set -x

root=$(readlink -f "$(dirname "$BASH_SOURCE")"/..)

# webserver
docker exec server_nginx_1 nginx -s reload

# mail
docker exec server_mailserver_1 service postfix reload
docker exec server_mailserver_1 service dovecot restart

# murmur
# See: https://wiki.mumble.info/wiki/Obtaining_a_Let's_Encrypt_Murmur_Certificate
docker exec server_murmur_1 pkill -USR1 murmurd

# jabber
uid=$(docker exec server_ejabberd_1 id -u ejabberd)
gid=$(docker exec server_ejabberd_1 id -g ejabberd)
cp /etc/letsencrypt/live/coldfix.de/{fullchain,privkey}.pem $root/var/ejabberd/ssl/
chown $uid:$gid $root/var/ejabberd/ssl/{fullchain,privkey}.pem
chmod 700 $root/var/ejabberd/ssl/{fullchain,privkey}.pem

# According to https://github.com/processone/ejabberd/issues/1109
# ejabberd automatically reloads SSL certificates, so no need for:
# docker exec -t server_ejabberd_1 /home/ejabberd/bin/ejabberdctl restart
docker exec -t server_ejabberd_1 /home/ejabberd/bin/ejabberdctl reload-config
