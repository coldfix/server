#! /bin/sh
set -e

port=64738
DB_FILE=/var/lib/murmur/murmur.sqlite

add_channel() {
    sqlite3 $DB_FILE "
        insert into channels
        (server_id, channel_id, parent_id, name, inheritacl) values
        (1, $1, 0, \"$3\", 1);
    "
    sqlite3 $DB_FILE "
        insert into channel_info
        (server_id, channel_id, key, value) values
        (1, $1, 0, \"\"),
        (1, $1, 1, \"$2\");
    "
}

/etc/murmur/sql_create_default_db.sh
add_channel 1  0 "Kätzchen"
add_channel 2 20 "Krümelchen"
add_channel 3 40 "Flauschetierchen"
add_channel 4 60 "Fette Torten"
