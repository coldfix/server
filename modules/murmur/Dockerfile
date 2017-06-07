FROM alpine:3.6

ENV INITMETHOD "sql"

COPY . /murmur
WORKDIR /murmur
VOLUME /etc/murmur
VOLUME /var/lib/murmur
VOLUME /var/log/murmur

RUN apk update && \
    apk add -u tini sqlite murmur icu-libs openssl

EXPOSE 64738/tcp
EXPOSE 64738/udp

ENTRYPOINT ["/sbin/tini", "--", "/murmur/init.sh"]
CMD ["/usr/sbin/murmurd", "-fg", "-v"]
