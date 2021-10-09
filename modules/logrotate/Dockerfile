FROM alpine:edge
COPY ./log_message.sh /opt/log_message.sh
RUN touch /var/log/messages
RUN apk add --no-cache tini dcron logrotate docker

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["crond", "-f", "-l", "info", "-M", "/opt/log_message.sh"]
