#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import logging
import MySQLdb
import json
import redis
import time

CONFIG_DIR = os.path.dirname(__file__)
sys.path.append(CONFIG_DIR)

from config import *

def _mysql_exec(sql):
    for config in DB_MASTER:
        try:
            conn = MySQLdb.connect(host=config['host'],
                           port=config['port'],
                           user=config['user'],
                           passwd=config['passwd'],
                           db=config['db_name'],
                           charset="utf8",
                           use_unicode=False)

            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            ret = cursor.fetchall()
            conn.close()
            return ret
        except Exception, msg:
            logging.error([('topic', '_mysql_exec'), ('key', "MySQLdb"), ('msg:', str(msg))])
            continue

    for config in DB_SLAVE:
        try:
            conn = MySQLdb.connect(host=config['host'],
                           port=config['port'],
                           user=config['user'],
                           passwd=config['passwd'],
                           db=config['db_name'],
                           charset="utf8",
                           use_unicode=False)
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            ret = cursor.fetchall()
            conn.close()
            return ret
        except Exception, msg:
            logging.error([('topic', '_mysql_exec'), ('key', "MySQLdb"), ('msg:', str(msg))])
            continue

    return []


def sync_redis_app():
    if len(RDS_HOST) == 0:
        return False

    sql = "select app_id,app_key,app_secret,is_encrypt,remark1,remark2 from gateway_app";
    apps = _mysql_exec(sql)
    if len(apps) == 0:
        logging.error([('topic', 'sync_redis_app'), ('key', "sync_redis_app() failed"), ("sql", sql)])
        return False

    st = {}
    for app in apps:
        st[app["app_id"]] = app

    json_value = json.dumps(st, ensure_ascii=False)
    print "apps"
    print json_value
    for config in RDS_HOST:
        try:
            rds = redis.Redis(host=config["host"], port=config["port"], db=0)
            rds.ping()
            rds.hset("__gateway_redis__", "shared_inner_app", json_value)
            rds.hset("__gateway_redis__", "app_update_time", int(time.time()))
            rds.save()
        except Exception, msg:
            logging.error([('topic', 'sync_gw_redis_app'), ('key', "Redis"), ("msg", str(msg))])
            return False
    logging.info([('topic', 'sync_gw_redis_app'), ('key', "sync to redis ok[app]")])

    return True


def sync_redis_limit():
    if len(RDS_HOST) == 0:
        return False

    sql = "select b.app_id, a.url, b.limit_value from gateway_service a, gateway_request_limit b where a.id=b.service_id"
    limits = _mysql_exec(sql)
    if len(limits) == 0:
        logging.error([('topic', 'sync_redis_limit'), ('key', "sync_redis_limit() failed"), ("sql", sql)])
        return False

    st = {}
    for limit in limits:
        st[limit["app_id"]] = {}

    for limit in limits:
        st[limit["app_id"]][limit["url"]] = limit["limit_value"]

    json_value = json.dumps(st, ensure_ascii=False)
    print "limits"
    print json_value
    for config in RDS_HOST:
        try:
            rds = redis.Redis(host=config["host"], port=config["port"], db=0)
            rds.ping()
            rds.hset("__gateway_redis__", "app_and_url_limit", json_value)
            rds.hset("__gateway_redis__", "limit_update_time", int(time.time()))
            rds.save()
        except Exception, msg:
            logging.error([('topic', 'sync_redis_limit'), ('key', "Redis"), ("msg", str(msg))])
            return False
    logging.info([('topic', 'sync_redis_limit'), ('key', "sync to redis ok[limit]")])

    return True


def main():
    sync_redis_app()
    sync_redis_limit()


if __name__ == '__main__':
    main()
