#!/bin/sh

DESTDIR=${DESTDIR-/usr/share/zabbix/externalscripts}

scripts="check_crt.py check_http check_rsync check_github_repo"
libs="jq.py"

for script in $scripts; do
    install -Dm0755 $script "$DESTDIR"/$script
done

for lib in $libs; do
    install -D lib/$lib "$DESTDIR/lib/$lib"
done
