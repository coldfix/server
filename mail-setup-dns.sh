#! /bin/bash

# Set up DNS records for mailserver.
#
# This wraps mail-setup-dns.py in a docker-container to remove the dependency
# on python packages on the host.
#
# For more details, see mail-setup-dns.py.

root=$(readlink -f $(dirname "$BASH_SOURCE"))

docker run --rm -it \
    -w / \
    -v "$root/mail-setup-dns.py":/mail-setup-dns.py \
    -v "$root/var/letsencrypt":/var/letsencrypt \
    -v "$root/var/mail/conf":/var/mail/conf \
    --cap-drop=all \
    coldfix/certbot-dns-netcup ./mail-setup-dns.py "$@"
