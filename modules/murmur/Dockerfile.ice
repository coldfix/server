FROM debian:8

ENV INITMETHOD "ice"

COPY . /murmur
WORKDIR /murmur
VOLUME /etc/murmur
VOLUME /var/lib/murmur
VOLUME /var/log/murmur

RUN apt-get update && \
    apt-get install -y mumble-server python-zeroc-ice

EXPOSE 64738/tcp
EXPOSE 64738/udp

ENTRYPOINT ["/murmur/init.sh"]
CMD ["/usr/bin/murmurd", "-fg", "-v"]
