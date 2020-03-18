#! /bin/bash
set -x

root=$(readlink -f $(dirname "$BASH_SOURCE"))

# webserver
# See: http://nginx.org/en/docs/beginners_guide.html#control
# See: http://nginx.org/en/docs/control.html
docker exec server_nginx_1 nginx -s reload
#docker exec server_nginx_1 pkill -HUP nginx
#docker exec server_nginx_1 sh -c 'kill -HUP $(cat /run/nginx.pid)'

# mail
systemctl reload postfix
systemctl restart dovecot

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
# docker restart server_ejabberd_1
