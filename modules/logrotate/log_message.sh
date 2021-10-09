#! /usr/bin/env sh
(
    echo '[[[--- cronjob'
    echo Date: `date`
    cat
    echo
    echo 'cronjob ---]]]'
) >> /var/log/cronjobs
