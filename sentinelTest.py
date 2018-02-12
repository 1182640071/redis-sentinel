#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 获取主服务器地址
from redis.sentinel import Sentinel

sentinel = Sentinel([('192.168.168.136',16379),
                    ('192.168.168.119',16379),
                    ('192.168.168.110',16379)],
                    socket_timeout=0.1,password='omygad911')

print sentinel.discover_master('mymaster6379')
# 输出：('192.168.168.136', 6379)

# 获取从服务器地址
print  sentinel.discover_slaves('mymaster6379')
# 输出：[('192.168.168.119', 6379), ('192.168.168.100', 6379)]

# 获取从服务器进行读取（默认是round-roubin）
slave = sentinel.slave_for('mymaster6379', socket_timeout=0.1)
print slave.keys()
print slave.hkeys('zabbix')
print slave.hget('zabbix','getTestMonitor_192.168.168.147')
# print slave.get('getMonitor_192.168.168.147')

# # 获取主服务器进行写入
master = sentinel.master_for('mymaster6379', socket_timeout=0.1)
print master.info()
# master.set('getMonitor_192.168.172.7', rs)