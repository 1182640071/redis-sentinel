#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

redis_fixed_text = """protected-mode no
tcp-backlog 511
timeout 0
tcp-keepalive 0
daemonize yes
supervised no
loglevel notice
databases 16
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
"""

configs = {
'port':"6379",
'pidfile':'"/var/run/redis-6379.pid"',
'logfile':'"/home/redis/log/redis-6379.log"',
'dbfilename':'"dump-6379.rdb"',
'dir':'"/home/redis/dump"',
'maxclients':'10240',
'maxmemory':'50g',
#'slave-priority':'100',
}

save = ['900 1', '300 10', '60 1000']

auth = ''

def write_redis_conf_master(configs, auth):
    file_name = "redis-%s-master.conf" % (configs['port'])
    with open(file_name, 'w+') as conf_file:
        conf_file.write(redis_fixed_text)
        for k,v in configs.items():
            conf_file.write("%s %s\n" % (k, v))
        if auth != '':
            conf_file.write('masterauth "%s"\nrequirepass "%s"\n' % (auth, auth))
        conf_file.write('slave-priority 100\n')

def write_redis_conf_slave(configs, auth, master_ip):
    file_name = "redis-%s-slave.conf" % (configs['port'])
    with open(file_name, 'w+') as conf_file:
        conf_file.write(redis_fixed_text)
        for k,v in configs.items():
            conf_file.write("%s %s\n" % (k, v))
        if auth != '':
            conf_file.write('masterauth "%s"\nrequirepass "%s"\n' % (auth, auth))
        conf_file.write('slaveof %s %s\n' % (master_ip, configs['port']))
        conf_file.write('slave-priority 110\n')

def write_redis_conf_dump(configs, auth, master_ip, save):
    file_name = "redis-%s-dump.conf" % (configs['port'])
    with open(file_name, 'w+') as conf_file:
        conf_file.write(redis_fixed_text)
        for k,v in configs.items():
            conf_file.write("%s %s\n" % (k, v))
        for i in save:
            conf_file.write("save %s\n" % (i))
        if auth != '':
            conf_file.write('masterauth "%s"\nrequirepass "%s"\n' % (auth, auth))
        conf_file.write('slaveof %s %s\n' % (master_ip, configs['port']))
        conf_file.write('slave-priority 120\n')

#port, user, maxclients, maxmemory, auth, master_ip
if __name__=="__main__":
    if len(sys.argv) != 7:
        input_port = raw_input("redis listen port:")
        input_user = raw_input("redis user:")
        input_maxcli = raw_input("redis maxclients:")
        input_maxmem = raw_input("redis maxmemory (GB):")
        auth = raw_input("redis auth password:")
        master_ip = raw_input("redis master ip:")
    else:
        input_port = sys.argv[1]
        input_user = sys.argv[2]
        input_maxcli = sys.argv[3]
        input_maxmem = sys.argv[4]
        auth = sys.argv[5]
        master_ip = sys.argv[6]
    configs['port'] = input_port
    configs['pidfile'] = '"/var/run/redis-%s.pid"' % (input_port)
    configs['logfile'] = '"/home/%s/log/redis-%s.log"' % (input_user, input_port)
    configs['dbfilename'] = '"dump-%s.rdb"' % (input_port)
    configs['dir'] = '"/home/%s/dump"' % (input_user)
    configs['maxclients'] = input_maxcli
    configs['maxmemory'] = '%sgb' % (input_maxmem)
    write_redis_conf_master(configs, auth)
    write_redis_conf_slave(configs, auth, master_ip)
    write_redis_conf_dump(configs, auth, master_ip, save)
