#! /bin/sh
set -ex

murmurd

# NOTE: for some reason there is no /var/run/murmur/murmur.pid
sleep 1
PID="`pgrep murmurd`"

kill $PID
wait $PID || echo "Exit status $?"
sleep 1
