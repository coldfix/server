Overview
========

This is the docker-compose configuration for my server at coldfix.de_. You may
adapt it to your purposes and use it for your own purposes. Note that this
repository is put under the GPLv3_.

.. _coldfix.de: https://coldfix.de
.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.en.html


Usage
~~~~~

.. code-block:: bash

    git clone git@github.com:coldfix/server --recursive
    cd server
    docker-compose up


Services
~~~~~~~~

`docker-compose up` will start the following sites/services:

- nginx with HTTP and HTTPS
- blog_     on coldfix.de_
- sudoku_   on sudoku.coldfix.de_
- gogs_     on gogs.coldfix.de_
- cryptpad_ on cryptpad.coldfix.de_
- goaccess_ on stats.coldfix.de_
- murmur_   on coldfix.de:64738
- ejabberd_ on coldfix.de

.. _blog:       https://github.com/coldfix/website
.. _sudoku:     https://github.com/coldfix/sudoku-swi
.. _gogs:       https://github.com/gogits/gogs
.. _cryptpad:   https://github.com/xwiki-labs/cryptpad
.. _goaccess:   https://github.com/allinurl/goaccess
.. _murmur:     https://github.com/mumble-voip/mumble
.. _ejabberd:   https://github.com/processone/ejabberd

.. _sudoku.coldfix.de:      https://sudoku.coldfix.de
.. _gogs.coldfix.de:        https://gogs.coldfix.de
.. _cryptpad.coldfix.de:    https://cryptpad.coldfix.de
.. _stats.coldfix.de:       https://statst.coldfix.de


maintenance
~~~~~~~~~~~

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


Missing
~~~~~~~

The following services running on coldfix.de_ are not yet dockerized:

- letsencrypt
- postfix/dovecot


Big TODOs
~~~~~~~~~

- drop privileges in all containers
