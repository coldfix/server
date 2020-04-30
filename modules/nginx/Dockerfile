FROM nginx:alpine

WORKDIR /nginx
COPY ./start.sh         /nginx/start.sh
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
CMD ["/nginx/start.sh"]
