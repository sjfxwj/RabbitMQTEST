#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',type='fanout')  #消息以后都是发送到exchange当中.

messages = ''.join(sys.argv[1:]) or 'info: Hello World!'
channel.basic_publish(exchange='logs',  #将消息发送到logs这个exchange当中.
                      routing_key='',   #routing_key现在没有什么用.
                      body=messages)

connection.close()