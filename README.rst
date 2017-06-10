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
- pypipins_ on pins.coldfix.de_
- murmur_   on coldfix.de:64738

.. _blog:       https://github.com/coldfix/website
.. _sudoku:     https://github.com/coldfix/sudoku-swi
.. _gogs:       https://github.com/gogits/gogs
.. _cryptpad:   https://github.com/xwiki-labs/cryptpad
.. _goaccess:   https://github.com/allinurl/goaccess
.. _pypipins:   https://github.com/coldfix/pypipins
.. _murmur:     https://github.com/mumble-voip/mumble

.. _sudoku.coldfix.de:      https://sudoku.coldfix.de
.. _gogs.coldfix.de:        https://gogs.coldfix.de
.. _cryptpad.coldfix.de:    https://cryptpad.coldfix.de
.. _stats.coldfix.de:       https://statst.coldfix.de
.. _pins.coldfix.de:        https://pins.coldfix.de


Missing
~~~~~~~

The following services running on coldfix.de_ are not yet dockerized:

- letsencrypt
- ejabberd
- postfix/dovecot
- logrotate