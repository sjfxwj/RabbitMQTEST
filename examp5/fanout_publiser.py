#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
rabbitmq中exchange的广播机制:
"""

import sys
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',type='fanout')  #logs为exchange的名字,没有声明队列
message = ' '.join(sys.argv[1:]) or 'Info:Hello World'   #生产者发送的消息

channel.basic_publish(exchange='logs',    #广播的时候不需要写Queue
                      routing_key='',     #注意:必须要写一个空
                      body=message)


print('[x] Sent %r'%message)

connection.close()

















