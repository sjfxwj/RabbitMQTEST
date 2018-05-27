#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
rabbitmq中exchange的广播机制:direct中的过滤模式
"""

import sys
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',exchange_type='direct')  #exchange的名字为direct_logs

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'   #重要程序(级别)
message = ' '.join(sys.argv[2:]) or 'Hello World'         #生产者发送的消息
#发布方不需要有queue,只需要有一个exchange就够了.

channel.basic_publish(exchange='direct_logs',    #广播的时候不需要写Queue
                      routing_key=severity,     #注意:必须要写一个空
                      body=message)


print('[x] Sent %r'%message)

connection.close()


