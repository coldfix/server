#! /usr/bin/env bash
docker run -it --rm \
    -v $(pwd)/var/mail/conf:/tmp/docker-mailserver \
    docker.io/mailserver/docker-mailserver setup "$@"
