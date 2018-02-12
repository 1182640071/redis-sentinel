#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sentinel_fixed_text = """daemonize yes
protected-mode no
"""

port = "2102"

master_instance = [["192.168.168.110", ["16379", ], ], ["192.168.168.111", ["16379", ], ]]
#master_instance = [["192.168.168.59", ["26380", "26384"], ], ["192.168.168.223", ["26379", "26383"], ], ["192.168.168.224", ["26382", "26386"]], ["192.168.168.225", ["26381", "26385"], ], ]

def write_sentinel_conf(sentinel_fixed_text, port, master_instance):
    file_name = "sentinel-%s.conf" % (port)
    with open(file_name, 'w+') as conf_file:
        conf_file.write(sentinel_fixed_text)
        conf_file.write("port %s\n" % (port))
        conf_file.write('logfile "./log/sentinel-%s.log"\n' % (port))
        for i in master_instance:
            for j in i[1]:  #["16380", ]
                conf_file.write("sentinel monitor mymaster%s %s %s 3\n" % (j, i[0], j))
                conf_file.write("sentinel down-after-milliseconds mymaster%s 3100\n" % (j))
                conf_file.write("sentinel failover-timeout mymaster%s 15000\n" % (j))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = raw_input("redis listen port:")
    write_sentinel_conf(sentinel_fixed_text, port, master_instance)