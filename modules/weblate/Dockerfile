FROM weblate/weblate

USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -y procps && \
    apt-get clean

USER weblate

ENTRYPOINT []
CMD /app/bin/start runserver
