Overview
========

This is the docker-compose configuration for my server at coldfix.de_. You may
adapt it to your purposes and use it for your own purposes. Note that this
repository is put under the GPLv3_.

.. _coldfix.de: https://coldfix.de
.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.en.html


Setup
~~~~~

.. code-block:: bash

    git clone git@github.com:coldfix/server --recursive
    cd server
    docker-compose up


mailserver
----------

The mailserver requires some initial setup:

- setup email and aliases using ``./mail-setup.sh [...]``, see setup.sh_
- create dkim keys: ``./mail-setup.sh config dkim``
- put netcup credentials in ``./var/letsencrypt/netcup_credentials.ini``, see
  Credentials_
- create DNS records, see `Best Practices`_::

    ./mail-setup-dns.sh \
        create-mx-record \
        create-spf-record \
        create-dkim-record \
        create-dmarc-record \
        list-records

- check DNS records using this `DMARC Guide`_, an `SPF Record Checker`_, and
  a `DKIM Key Checker`

.. _setup.sh:           https://docker-mailserver.github.io/docker-mailserver/edge/config/setup.sh/
.. _Best Practices:     https://docker-mailserver.github.io/docker-mailserver/edge/config/best-practices
.. _Credentials:        https://github.com/coldfix/certbot-dns-netcup#credentials
.. _DMARC Guide:        https://dmarcguide.globalcyberalliance.org/
.. _SPF Record Checker: https://www.dmarcanalyzer.com/spf/checker/
.. _DKIM Key Checker:   https://protodave.com/tools/dkim-key-checker/


Services
~~~~~~~~

`docker-compose up` will start the following sites/services:

- nginx with HTTP and HTTPS
- blog_     on coldfix.de_
- sudoku_   on sudoku.coldfix.de_
- gogs_     on gogs.coldfix.de_
- murmur_   on coldfix.de:64738
- ejabberd_ on coldfix.de
- docker-mailserver_ on coldfix.de

.. _blog:                   https://github.com/coldfix/website
.. _sudoku:                 https://github.com/coldfix/sudoku-swi
.. _gogs:                   https://github.com/gogits/gogs
.. _murmur:                 https://github.com/mumble-voip/mumble
.. _ejabberd:               https://github.com/processone/ejabberd
.. _docker-mailserver:      https://github.com/docker-mailserver/docker-mailserver

.. _sudoku.coldfix.de:      https://sudoku.coldfix.de
.. _gogs.coldfix.de:        https://gogs.coldfix.de


maintenance
~~~~~~~~~~~

mailserver
----------

See: https://docker-mailserver.github.io/docker-mailserver/edge/

letsencrypt
-----------

letsencrypt cronjob is currently not run within docker container because it
needs to restart the mail system which is not yet dockerized. You need to setup
a cronjob like this manually:

.. code-block:: crontab

    # min   hour    dom     mon     dow     cmd
    0       5,21    *       *       *       /home/server/cert-renew.sh --wait 60 --quiet

ejabberd
--------

Create backup:

.. code-block:: bash

    docker exec server_ejabberd_1 /usr/local/sbin/ejabberdctl backup /opt/ejabberd/backup/ejabberd.backup
    docker cp server_ejabberd_1:/opt/ejabberd/backup/ejabberd.backup /tmp/ejabberd.backup

Restore backup:

.. code-block:: bash

    docker cp /tmp/ejabberd.backup server_ejabberd_1:/opt/ejabberd/backup/ejabberd.backup
    docker exec server_ejabberd_1 /usr/local/sbin/ejabberdctl restore /opt/ejabberd/backup/ejabberd.backup

Create admin user:

.. code-block:: bash

    docker exec server_ejabberd_1 \
        /usr/local/sbin/ejabberdctl register admin coldfix.de "password"

Replace SSL certificate:

.. code-block:: bash

    uid=$(docker exec server_ejabberd_1 id -u ejabberd)
    gid=$(docker exec server_ejabberd_1 id -g ejabberd)
    crt=$(pwd)/var/ssl/ejabberd.pem
    cat /etc/letsencrypt/live/coldfix.de/{fullchain,privkey}.pem $crt
    chown $uid:$gid $crt
    chmod 700 $crt
    docker restart server_ejabberd_1


Big TODOs
~~~~~~~~~

- drop privileges in all containers
