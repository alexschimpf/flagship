#!/usr/bin/env bash

MYSQL_USER=root
MYSQL_PASSWORD=test
chown -R mysql:mysql /var/lib/mysql

mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "DROP DATABASE IF EXISTS flagship"
mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE flagship DEFAULT CHARACTER SET utf8;"

mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -D flagship < /opt/sql/flagship.sql
