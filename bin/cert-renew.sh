#! /bin/bash

#docker pull certbot/dns-netcup > /dev/null

root=$(readlink -f "$(dirname "$BASH_SOURCE")"/..)
source "$root/etc/cert-config.sh"

if [[ $1 = "--wait" ]]; then
    sleep $(expr $RANDOM % $2)m
    shift 2
fi

# NOTE: for renewal only, we could simply run `renew --renew-hook HOOK`
# NOTE: to force renewal, replace '--keep-until-expiring' with '--renew-by-default'
docker run --rm \
    -v "$root/var/letsencrypt":/var/lib/letsencrypt \
    -v /etc/letsencrypt:/etc/letsencrypt \
    --cap-drop=all \
    coldfix/certbot-dns-netcup certbot certonly \
        --authenticator dns-netcup \
        --dns-netcup-credentials /var/lib/letsencrypt/netcup_credentials.ini \
        --dns-netcup-propagation-seconds 900 \
        --keep-until-expiring --non-interactive --expand \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --email "$email" --text --agree-tos \
        --renew-hook 'touch /var/lib/letsencrypt/.updated' \
        ${domains[@]/#/-d } "$@"

# old server ip: 88.198.213.2
docker run --rm \
    -v "$root/var/letsencrypt":/var/lib/letsencrypt \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -v $(pwd)/var/acme:/var/www \
    coldfix/certbot-dns-netcup certbot certonly \
        --keep-until-expiring --non-interactive --expand \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --renew-hook 'touch /var/lib/letsencrypt/.updated' \
        --email "tapienz@gmail.com" --text --agree-tos \
        --webroot --webroot-path /var/www \
        -d miosta.eu -d www.miosta.eu -d gogs.miosta.eu "$@"

if rm "$root/var/letsencrypt/.updated" 2>/dev/null; then
    exec "$root/bin/cert-reload.sh"
fi
