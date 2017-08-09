#! /bin/bash

docker pull certbot/certbot > /dev/null

root=$(readlink -f $(dirname "$BASH_SOURCE"))
source "$root/cert-config.sh"

if [[ $1 = "--wait" ]]; then
    sleep $(expr $RANDOM % $2)m
    shift 2
fi

# NOTE: for renewal only, we could simply run `renew --renew-hook HOOK`
# NOTE: to force renewal, replace '--keep-until-expiring' with '--renew-by-default'
docker run --rm \
    -v "$root/var/acme":/var/www \
    -v "$root/var/letsencrypt":/var/lib/letsencrypt \
    -v /etc/letsencrypt:/etc/letsencrypt \
    --cap-drop=all \
    certbot/certbot certonly --no-self-upgrade \
        --keep-until-expiring --non-interactive \
        --email "$email" --text --agree-tos \
        --webroot -w /var/www  \
        --renew-hook 'touch /var/www/.updated' \
        ${domains[@]/#/-d } "$@"

if rm "$root/var/acme/.updated" 2>/dev/null; then
    exec "$root/cert-reload.sh"
fi
