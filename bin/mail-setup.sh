#! /usr/bin/env bash
root=$(readlink -f "$(dirname "$BASH_SOURCE")"/..)
docker run -it --rm \
    -v "$root/var/mail/conf":/tmp/docker-mailserver \
    docker.io/mailserver/docker-mailserver setup "$@"
