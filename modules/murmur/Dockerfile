FROM alpine:3.6

ENV INITMETHOD "sql"

COPY . /murmur
WORKDIR /murmur
VOLUME /etc/murmur
VOLUME /var/lib/murmur
VOLUME /var/log/murmur

RUN apk add --no-cache sqlite murmur icu-libs openssl

EXPOSE 64738/tcp
EXPOSE 64738/udp

ENTRYPOINT ["/murmur/init.sh"]
CMD ["/usr/bin/murmurd", "-fg", "-v"]
