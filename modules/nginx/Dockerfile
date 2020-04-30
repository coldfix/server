FROM nginx:alpine

COPY ./logrotate.conf   /etc/logrotate.conf
COPY ./crontab          /etc/crontabs/root

RUN apk update && \
    apk add -u tini bash logrotate && \
    rm -rf /etc/nginx

VOLUME /etc/nginx
VOLUME /etc/letsencrypt
VOLUME /var/www/blog
VOLUME /var/log/nginx
EXPOSE 80 443

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/bin/sh", "-c", "crond && nginx -g 'daemon off;'"]
