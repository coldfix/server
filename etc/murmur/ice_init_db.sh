#! /bin/bash

mkdir -p /murmur/ices
cd /murmur/ices
slice2py -I/usr/share/Ice-3.5.1/slice /usr/share/slice/Murmur.ice

( sleep 10s && /etc/murmur/ice_setup_murmur_server.sh ) &
