#! /bin/sh
set -ex

# Get the mounted config file if it exists:
[ -f /etc/murmur/murmur.ini ] && cp /etc/murmur/murmur.ini /etc/murmur.ini

# Create data folders and adjust permissions:
mkdir -p /var/lib/murmur && chown -R murmur:murmur /var/lib/murmur
mkdir -p /var/log/murmur && chown -R murmur:murmur /var/lib/murmur

# Setup an initial database file:
if  [ -x /etc/murmur/${INITMETHOD}_init_db.sh ] && [ ! -f /var/lib/murmur/murmur.sqlite ]; then
    /etc/murmur/${INITMETHOD}_init_db.sh
fi

# Spawn process
exec "$@"
