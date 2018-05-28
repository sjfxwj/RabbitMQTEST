#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.basic_publish(exchange='logs',        #将消息发送到logs这个exchange当中.
                      routing_key='',         #routing_key现在没有什么用.
                      body='fantout message')

connection.close()    #此时此刻的功能同redis
