#! /bin/bash

echo "[$(date)] Running $@"
set -x

root=$(readlink -f "$(dirname "$BASH_SOURCE")"/..)


if [[ $1 = "--wait" ]]; then
    sleep $(expr $RANDOM % $2)m
    shift 2
fi
date


# old server ip: 88.198.213.2
docker run --rm \
    -v "$root/var/letsencrypt":/var/lib/letsencrypt \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -v "$root/var/acme:/var/www" \
    coldfix/certbot-dns-netcup certbot certonly \
        --keep-until-expiring --non-interactive --expand \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --renew-hook 'touch /var/lib/letsencrypt/.updated-miosta' \
        --email "tapienz@gmail.com" --text --agree-tos \
        --webroot --webroot-path /var/www \
        -d miosta.eu -d www.miosta.eu -d gogs.miosta.eu "$@"
date



if rm "$root/var/letsencrypt/.updated-miosta" 2>/dev/null; then
    docker exec server_nginx_1 nginx -s reload
    date
fi
