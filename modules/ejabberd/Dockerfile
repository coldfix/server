FROM ejabberd/ecs

USER root
RUN apk update && apk add -u dumb-init
USER ejabberd

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/home/ejabberd/bin/ejabberdctl", "foreground"]
