#! /bin/bash

#docker pull certbot/dns-netcup > /dev/null

root=$(readlink -f $(dirname "$BASH_SOURCE"))
source "$root/cert-config.sh"

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
    certbot/dns-netcup certonly \
        --authenticator certbot-dns-netcup:dns-netcup \
        --certbot-dns-netcup:dns-netcup-credentials /var/lib/letsencrypt/netcup_credentials.ini \
        --certbot-dns-netcup:dns-netcup-propagation-seconds 900 \
        --no-self-upgrade \
        --keep-until-expiring --non-interactive --expand \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --email "$email" --text --agree-tos \
        --renew-hook 'touch /var/lib/letsencrypt/.updated' \
        ${domains[@]/#/-d } "$@"

if rm "$root/var/letsencrypt/.updated" 2>/dev/null; then
    exec "$root/cert-reload.sh"
fi
