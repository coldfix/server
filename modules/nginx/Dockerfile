FROM alpine:edge

RUN apk update && \
    apk add -u nginx tini bash && \
    rm -rf /etc/nginx && \
    adduser -u 1000 -D -S -G www-data www-data && \
    mkdir -p /var/log/nginx /var/tmp/nginx/client_body && \
    chown www-data:www-data /var/tmp/nginx/client_body && \
    chmod 755 /var /var/tmp /var/tmp/nginx

VOLUME /etc/nginx
VOLUME /etc/letsencrypt
VOLUME /var/www/blog
VOLUME /var/www/pypi
VOLUME /var/log/nginx
EXPOSE 80 443

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["nginx", "-g", "daemon off;"]
