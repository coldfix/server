FROM python:3.8-alpine

ENV build_deps="git gcc musl-dev libffi libffi-dev openssl-dev"
ENV runtime_deps="openssl"

RUN apk update && \
    apk add -u $runtime_deps $build_deps && \
    pip install certbot && \
    pip install git+https://github.com/coldfix/certbot-dns-netcup.git@master && \
    apk del $build_deps
