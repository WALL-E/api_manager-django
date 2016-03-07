#-*- encoding: utf-8 -*-

import os
import sys

CONFIG_DIR = os.path.dirname(__file__)
sys.path.append(CONFIG_DIR)
# sys.path.append(os.path.join(CONFIG_DIR, 'libs'))

# from mysql import MysqlClient

# 数据库配置
DB_NAME = 'api_manager'

DB_MASTER = [{'db_name': DB_NAME,
              'host': '127.0.0.1',
              'user': 'root',
              'passwd': '',
              'port': 3306}]

DB_SLAVE = [{'db_name': DB_NAME,
             'host': '127.0.0.1',
             'user': 'root',
             'passwd': '',
             'port': 3306}]

# MYSQL_CLIENT = MysqlClient(DB_MASTER, DB_SLAVE)

RDS_HOST = [{'host':'127.0.0.1', 'port':6379}]
